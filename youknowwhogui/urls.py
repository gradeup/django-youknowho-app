from django.conf.urls import url

from .views import *

urlpatterns = [

  url(r'rules/', RulesList.as_view(), name='rules_list'),
  url(r'simulate/', RulesSimulate.as_view(), name='rule_simulation'),

]
