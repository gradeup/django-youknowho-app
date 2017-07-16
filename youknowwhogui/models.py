from django.db import models

from myghanta.fields import MysqlTimeStampField


class RuleTag(models.Model):
    tag_name = models.CharField(primary_key=True, max_length=255)
    created_at = MysqlTimeStampField(auto_now_add=True, blank=True, null=True)
    updated_at = MysqlTimeStampField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        db_table = 'rule_tag'


class Rule(models.Model):

    RULE_STATUS = (
        ( 1, 'Enabled'),
        ( 0, 'Disabled')
    )

    RULE_OPERATOR = (
       ( '&&', 'AND ( && )'),
       ( '||', 'OR ( || )'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True, help_text='For personal reference. Not used anywhere in logic')
    tags = models.ManyToManyField(RuleTag, db_table='rule_ruletag', blank=True)
    external_reference = models.CharField(max_length=255, blank=True,)
    status = models.IntegerField(choices=RULE_STATUS, default=1)
    priority = models.IntegerField(blank=True, null=True, help_text='Priority 1 is highest. Lower the number higher the priority.')
    conditions_operator = models.CharField(max_length=255, blank=True, choices=RULE_OPERATOR,
        help_text='Please select if rule conditions should be ANDed or ORed.. By default AND is selected', default='&&')
    created_at = MysqlTimeStampField(auto_now_add=True, blank=True, null=True)
    updated_at = MysqlTimeStampField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        permissions = (
            ('CAN_ENABLE_RULE', 'Can Enable rule'),
            ('CAN_DISABLE_RULE', 'Can Disable rule'),
        )
        db_table = 'rule'


class RuleActionKeys(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'rule_action_keys'
        verbose_name_plural = 'Rule Action Keys'


class RuleAction(models.Model):

    ACTION_CHOICE = (
        ('SET_VARIABLE', 'Set Variable'),
        ('SET_NUMBER', 'Set Number'),
        ('DANGEROUS_EVAL', 'Evaluate'),
        ('RE_EXIT', 'Stop Processing more rules'),
    )

    rule = models.ForeignKey(Rule)
    description = models.TextField(blank=True, null=True, help_text='For personal reference. Not used anywhere in logic')
    action = models.CharField(max_length=255, choices=ACTION_CHOICE)
    key = models.ForeignKey(RuleActionKeys, db_column='key', null=True, blank=True)
    value = models.TextField(blank=True, null=True,
        help_text='''Can have STRING ( TEMPLATED or NORMAL), BOOLEAN \
        E.g.  true, false are boolean values . \
        Almost all message properties can be used as variables \
        like <%= userdata.amount %> <%= userdata.recharge_number %>''')
    created_at = MysqlTimeStampField(auto_now_add=True, blank=True, null=True)
    updated_at = MysqlTimeStampField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.rule_id)

    class Meta:
        db_table = 'rule_action'


class RuleConditionKeys(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'rule_condition_keys'
        verbose_name_plural = 'Rule Condition Keys'


class RuleCondition(models.Model):

    RULE_OPERATIONS = (
        ( '=', 'Equals ( = )'),
        ( '!=', 'Not Equals ( != )'),

        ( '>', 'Great than Integer ( > )'),
        ( '>=', 'Great than Equals Integer( >= )'),

        ( '<', 'Less than Integer( < )'),
        ( '<=', 'Less than Equals Integer( <= )'),

        ('range', 'In Numerical Range ( range )'),
        ('!range', 'Not In Numerical Range ( !range )'),

        ('datetimerange', 'In DateTime Range ( datetimerange )'),
        ('!datetimerange', 'Not In DateTime Range ( !datetimerange )'),

        ('timerange', 'In Time Range ( timerange )'),
        ('!timerange', 'Not In Time Range ( !timerange )'),

        ('regex', 'In Regex ( regex )'),
        ('!regex', 'Not In Regex ( !regex )'),

        ('includesstring', 'Array Contains String ( includesstring )'),
        ('!includesstring', 'Array Does Not Contains String ( !includesstring )'),

        ('includesint', 'Array Contains Integer ( includesint )'),
        ('!includesint', 'Array Does Not Contains Integer ( !includesint )'),

        ('stringrange', 'In String Array ( stringrange )'),
        ('!stringrange', 'Not In String Array ( !stringrange )'),

        ('set', 'Is In Set(set)'),
        ('!set', 'Is Not In Set(!set)'),
     )

    RULE_CONDITIONS = (
        ('checkvariable', 'Check Variable'),
    )

    rule = models.ForeignKey(Rule)
    key = models.ForeignKey(RuleConditionKeys, db_column='key', null=True, blank=True)
    description = models.TextField(blank=True, null=True, db_column='description', help_text='For personal reference. Not used anywhere in logic')
    condition = models.CharField(max_length=255, choices=RULE_CONDITIONS, blank=False, null=False, default='checkvariable')
    operation = models.CharField(max_length=255, choices = RULE_OPERATIONS, blank=False, null=False)
    value = models.TextField(blank=False, null=False,
        help_text ='''Different values for different operations. \
        Such as range can have numerical ranges like 1,2,4~5, 6~10,11,12~ . \
        datetimerange can have range like 2015-06-11 ~ 2015-07-12 .''')
    created_at = MysqlTimeStampField(auto_now_add=True, blank=True, null=True)
    updated_at = MysqlTimeStampField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.rule_id)

    class Meta:
        db_table = 'rule_condition'
