import json
import requests

from collections import OrderedDict

from django.conf import settings
from django.forms import formset_factory
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .forms import RuleConditionKeysForm, RuleTagForm
from .models import Rule


class RulesList(ListView):

    '''
        returns a list of rules, like

        [{
          "id": 1,
          "name": "Natural Number ",
          "external_reference": "",
          "conditionsOperator": "&&",
          "priority": 170001,
          "tags": [
            "natural",
          ],
          "conditions": [{
            "id": 1,
            "key": "integer",
            "operation": ">",
            "value": "0"
          }],
          "actions": [{
            "id": 2,
            "action": "SET_VARIABLE",
            "key": "is_natural",
            "value": 1
          }]
        }]
    '''

    def get(self, request, *args, **kwargs):
        output_json = {}
        rules = Rule.objects.all().order_by('-id')
        rules_arr = []
        for each_rule in rules:
            temp_rule = {}
            temp_rule['id'] = each_rule.id
            temp_rule['name'] = each_rule.name.strip()
            temp_rule['externalReference'] = each_rule.external_reference.strip()
            temp_rule['priority'] = each_rule.priority
            temp_rule['conditionsOperator'] = each_rule.conditions_operator.strip()
            rule_tags = list(each_rule.tags.all().values_list('tag_name', flat=True)) or []
            temp_rule['tags'] = rule_tags

            # rule actions
            rule_actions = each_rule.ruleaction_set.select_related('key').all() or []
            actions_arr = []
            for each_action in rule_actions:
                temp_action = {}
                temp_action['id'] = each_action.id
                temp_action['action'] = each_action.action.strip()
                temp_action['key'] = each_action.key.name.strip()
                temp_action['value'] = each_action.value.strip()

                if temp_action['id']:
                    actions_arr.append(temp_action)
            temp_rule['actions'] = actions_arr

            # rule conditions
            rule_conditions = each_rule.rulecondition_set.select_related('key').all() or []
            conditions_arr = []
            for each_condition in rule_conditions:
                temp_condition = {}
                temp_condition['id'] = each_condition.id
                temp_condition['operation'] = each_condition.operation.strip()
                temp_condition['key'] = each_condition.key.name.strip()
                temp_condition['value'] = each_condition.value.strip()

                if temp_condition['id']:
                    conditions_arr.append(temp_condition)
            temp_rule['conditions'] = conditions_arr

            if temp_rule.get('id'):
                rules_arr.append(temp_rule)

        output_json['rules'] = rules_arr
        return JsonResponse(output_json)


class RulesSimulate(ListView):

    template_name = 'simulation.html'
    condition_form = RuleConditionKeysForm
    tag_form = RuleTagForm

    def get(self, request, *args, **kwargs):
        RuleConditionKeysFormSet = formset_factory(self.condition_form_class)
        formset = self.condition_form(request.GET or None)
        tag_form = self.tag_form(request.GET or None)
        rEInput = {}
        requestInfo = {}
        actionInfo = {}
        rules_response = []
        rule_condition_map = {}
        formset_length = 0
        rETag = None
        if tag_form.is_valid():
            rETag = tag_form.cleaned_data.get('tag', None)

        if formset.is_valid():
            for form in formset:
                condition_key = form.cleaned_data.get('condition_key')
                condition_value = form.cleaned_data.get('condition_value')
                if not condition_key:
                    continue
                condition_key = condition_key.name
                rEInput[condition_key] = condition_value

            post_data = {
                'input': rEInput,
            }
            headers = {
                'Content-Type': 'application/json',
                'X-Client-Id': settings.RULE_ENGINE_X_CLIENT_ID,
            }
            if rETag:
                post_data['tag'] = rETag
            url = settings.RULE_ENGINE_SIMULATION_URL + settings.RULE_ENGINE_SIMULATION_API_ENDPOINT
            try:
                response = requests.get(url, data=json.dumps(post_data), headers=headers, timeout=10)
            except Exception as e:
                print 'Failed to request rule engine for simulation {}'.format(e)
                response = None

            if response and response.status_code == 200:
                parsed_response = json.loads(response.text)
                rules_map = parsed_response.get('meta', {}).get('rules', {})
                requestInfo = json.dumps(parsed_response.get('requestInfo', {}), indent=4)
                actionInfo = json.dumps(parsed_response.get('actionInfo', {}), indent=4)
                # so that condition can be extracted only specific to these rules
                rule_ids = rules_map.keys()
                rules_response = [v for (k,v) in rules_map.items()]
                # so that rules are displayed in order they were applied.
                rules_response.sort(key=lambda x: x['exec_order'])
                # for better template formatting,
                rule_conditions = RuleCondition.objects.filter(rule__id__in=rule_ids)
                for condition in rule_conditions:
                    rule_condition_map[str(condition.id)] = {
                        'id': condition.id,
                        'key': condition.key.name,
                        'condition': condition.condition,
                        'operation': condition.operation,
                        'value': condition.value
                    }
        # so that last form can be detected and plus sign can be displayed against it
        formset_length = len(formset)
        return render(request, self.template_name, {
            'formset': formset,
            'tag_form': tag_form,
            'rules_response': rules_response,
            'conditions_map': rule_condition_map,
            'requestInfo': requestInfo,
            'actionInfo': actionInfo,
            'last_form_counter': formset_length
        })
