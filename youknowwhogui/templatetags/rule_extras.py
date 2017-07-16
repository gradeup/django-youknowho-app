from django import template

register = template.Library()


@register.filter(name='lookup')
def cut(dict_obj, key):
    return dict_obj.get(key, {})
