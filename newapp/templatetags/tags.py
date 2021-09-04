from django import template

register = template.Library()

@register.filter
def has_attr(user, usertype):
    return hasattr(user, usertype)
