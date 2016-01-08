# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.

from settings.models import addGlobalContext
from .models import GenericField, GenericFieldLink


def home(request):
    return render(request,"miscFields/home.html", context=addGlobalContext(
        {
            'all_fields': GenericField.objects.all()
            }))


def editField(request, id):
    if id != None:
        generic_field = GenericField.objects.get(id=id)
    else:
        generic_field = None
    context = {
                "generic_field": generic_field
            }
    return render(request, "miscfield/editField.html",addGlobalCOntext(context))
