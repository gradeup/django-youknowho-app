import re

from django import forms
from django.forms import ModelForm

from .models import *

class RuleConditionForm(ModelForm):

    class Meta:
        model = RuleCondition
        fields = ('condition', 'key', 'operation', 'value',)
        widgets = {
            'value': forms.Textarea(attrs={'rows': 1}),
            'description': forms.TextInput()
        }

    def clean(self):
        form_data       = self.cleaned_data
        if form_data['operation'] in ['range', '!range']:
            form_data['value'] = form_data['value'].replace('\n', ' ').replace('\r', '')
            matchObj = re.search(r'[^0-9,~ ]+', form_data['value'])
            if matchObj:
                raise forms.ValidationError(u'Allowed Characters : Digits and ~ when selecting Range or !Range')
        return form_data

class RuleActionForm(ModelForm):

    class Meta:
        model = RuleAction
        fields = ('action', 'key', 'value', )
        widgets = {
            'value': forms.Textarea(attrs={'rows': 1}),
            'description': forms.TextInput()
        }


class RuleTagForm(forms.Form):

    tag = forms.ChoiceField(
        label='Rule Tag',
        required=False,
        help_text='Specify Rule Tag here',
        choices=(),
        widget = forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select Rule Tag',
            'style': 'width : 100%'
        })
    )

    def __init__(self, *args, **kwargs):
        super(RuleTagForm, self).__init__(*args, **kwargs)
        choices = [('', '')] + [(tag.tag_name, tag.tag_name) for tag in RuleTag.objects.all()]
        self.fields['tag'].choices = choices


class RuleConditionKeysForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(RuleConditionKeysForm, self).__init__(*args, **kwargs)
        self.fields['condition_key'] = forms.ModelChoiceField(
            queryset=RuleConditionKeys.objects.all(),
            label='Condition Key',
            required=False,
            help_text='Specify Condition Key here',
            widget = forms.Select(attrs={
                'class': 'form-control condition-element',
            })
        )
        self.fields['condition_value'] = forms.CharField(
            label='Condition Value',
            help_text='Specify condition value here',
            widget= forms.TextInput(attrs={
                'class': 'form-control condition-element',
                'placeholder' : 'Condition Value',
            })
        )
