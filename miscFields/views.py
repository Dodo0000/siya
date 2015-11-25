from django.shortcuts import render

# Create your views here.

from settings.models import addGlobalContext
from .models import GenericField, GenericFieldLink


def home(request):
    return render(request,"miscFields/home.html", context=addGlobalContext(
        {
            'all_fields': GenericField.objects.all()
            }))
