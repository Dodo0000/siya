from django.shortcuts import render
from django.contrib.auth.models import Group, Permission

from settings.models import addGlobalContext
# Create your views here.


def home(request):
    all_groups = Group.objects.all()
    context = addGlobalContext({
        "all_groups": all_groups,
        })
    return render(request,'almsGroups/home.html',context=context)


def addGroup(request):
    all_perms = Permission.objects.all()
    context = addGlobalContext({
                    "all_permissions": all_perms
                })
    return render(request, 'almsGroups/new.html', context=context)
