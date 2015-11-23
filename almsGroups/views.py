from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required

from settings.models import addGlobalContext
# Create your views here.


@login_required(login_url="/login")
def homeWithArgs(request,group_added,group_name):
    all_groups = Group.objects.order_by("-id")
    context = addGlobalContext({
        "all_groups": all_groups,
        "group_added": False,
        "group_name": group_name
        })
    return render(request,'almsGroups/home.html',context=context)


@login_required(login_url="/login")
def home(request):
    return homeWithArgs(request,group_added=False,group_name=None)


@login_required(login_url="/login")
def addGroup(request):
    all_perms = Permission.objects.filter(Q(codename__contains="Book")|Q(codename__contains="ModUser"))
    if request.method == "POST":
        name = request.POST.get("name", None)
        if name != None:
            groups = Group.objects.filter(name=name)
            if len(groups) > 0:
                group_exists = True
            else:
                group_exists = False
            permissions = {}
            for perm in all_perms:
                permissions[perm.codename] = request.POST.get("perm_"+perm.codename,False)
            if group_exists is False:
                group = Group.objects.create(name=name)
            else:
                group = groups[0]
            for perm in permissions.items():
                if perm[1] is not False:
                    try:
                        group.permissions.get(codename=perm[0])
                    except ObjectDoesNotExist:
                        group.permissions.add(Permission.objects.get(codename=perm[0]))
            group.save()
            group_added = True
        else:
            group_added = False ## name is None
    else:
        group_added = None  ## POST Request not sent

    if group_added is True:
        return HttpResponseRedirect(reverse("almsGroupsHomeWithArgs", kwargs={"group_added":int(True),"group_name":smart_str(group.name) }))

    elif group_added is False:
        context = addGlobalContext({
                        "all_permissions": all_perms,
                        'group_added': int(group_added),
                        'group': group
                    })
    else:
        context = addGlobalContext({
                        "all_permissions": all_perms,
                    })


    return render(request, 'almsGroups/new.html', context=context)
