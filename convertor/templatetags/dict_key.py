from django import template

register = template.Library()


@register.simple_tag
def get_values_from_dictionary_tag(dictionary, key):
    return dictionary.get(key)
