from django import template

register = template.Library()

@register.filter(name='user_greeting_name')
def user_greeting_name(value):
    """Generate a name to be used for greeting a user"""
    if value.first_name is not None and value.first_name != '':
        return value.first_name
    else:
        return value.username
