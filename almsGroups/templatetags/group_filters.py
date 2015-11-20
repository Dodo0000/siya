from django import template

register = template.Library()

@register.filter(name='getFormattedPermissions')
def getFormattedPermissions(value):
    return ' '.join([
        '<span class="label label-primary">{}</span>'.format(_.name) for _ in value
        ])
