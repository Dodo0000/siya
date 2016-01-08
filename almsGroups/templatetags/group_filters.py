# -*- coding: utf-8 -*-
from django import template
from django.db.models import Q


register = template.Library()

@register.filter(name='getFormattedPermissions')
def getFormattedPermissions(value):
    if len(value)== 0:
        return "No Permissions"
    else:
        return ' '.join([
            '<span class="label label-primary">{}</span>'.format(_.name) for _ in value
            ])

@register.filter(name="getReasonablePermissions")
def getReasonablePermission(value):
    return value.permissions.filter(Q(codename__contains="ModUser")|Q(codename__contains="Book"))


@register.filter(name="makeGlyphicon")
def makeGlyphicons(value):
    value = str(value)
    if value.isdigit():
        temp = '<span class="glyphicon glyphicon-{}"></span>'
        return temp.format(value)
    else:
        return ""

@register.filter(name="hasPerm")
def hasPerm(value, arg):
    return int(len(value.permissions.filter(codename=arg)) > 0)
