# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template


from settings.models import Globals

from pyBSDate.BSDate import convert_to_bs

register = template.Library()

NONE_LS = [None, "None"]

config = Globals()


@register.filter(name="tobs")
def to_bs(value):
    if value.__class__ not in [unicode, str]:
        try:
            value = value.isoformat()
        except:
            raise TypeError("value doesn't have isoformat method")
    np_date = convert_to_bs(value)
    return np_date
