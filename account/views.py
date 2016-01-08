# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.utils.encoding import smart_str

from .models import ModUser
from .forms import CreateMemberForm
from head.models import Book, Lend
from head.views import home
from settings.models  import addGlobalContext

from settings.models import Globals

import datetime
# Create your views here.

config = Globals()


@login_required(login_url="/login")
def profile(request, username):
    config.refresh()
    user = get_object_or_404(ModUser, username=username)
    books_borrowed = Lend.objects.filter(user=user, returned=False)
    len_books_borrowed = len(books_borrowed)
    return render(
        request,
        'account/user.html',
        addGlobalContext(
            {
                'globals': config,
                'date': datetime.date.today(),
                'search_user': user,
                'books_borrowed': books_borrowed,
                'len_books_borrowed': len_books_borrowed
                }
            ))


@login_required(login_url="/login")
def search_member(request):
    config.refresh()
    import string
    username = request.GET.get("username", None)
    if username is not None:
        user = ModUser.objects.filter(username=username)
        if len(user) == 1:
            user = user[0]
            return HttpResponseRedirect(reverse('profile', kwargs={"username": user.username}))
        else:
            return render(request, 'account/search_user.html', addGlobalContext({'not_found': True, 'username': username, "alphabets": string.ascii_lowercase, 'globals': config, 'date': datetime.date.today()}))
    else:
        return render(request, 'account/search_user.html', addGlobalContext({"alphabets": string.ascii_lowercase,"globals": config, 'date': datetime.date.today()}))




def login_get_code_msg(code):
    config.refresh()
    if code == 0:
        return "Login Successful"
    elif code == 1:
        return "User is not Active"
    elif code == 2:
        return "Invalid login credentials"
    elif code == 3:
        return "Login Form Method was not POST"
    elif code == 4:
        return ""
    else:
        return None



def login_user(request):
    config.refresh()

    '''
    code values and their meaning : 
    0 : Login Successful
    1 : User is Not Active! Accoutn disabled
    2 : Invalid Login creds!
    3 : request method was not POST
    '''
    code = None

    LOGIN_SUCCESS = 0
    USER_NOT_ACTIVE = 1
    INVALID_LOGIN_CREDS = 2
    METHOD_NOT_POST = 3
    NO_DATA_GIVEN = 4

    if request.method.upper() == "POST":
        username = unicode(request.POST.get("username", None))
        password = unicode(request.POST.get("password", None))


        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                code = LOGIN_SUCCESS
            else:
                code = USER_NOT_ACTIVE ## user is not active
        else:
            code = INVALID_LOGIN_CREDS ## invalid login creds
    else:
        if unicode(request.POST.get('username', None)) is not None and unicode(request.POST.get("password", None)) is not None:
            code = METHOD_NOT_POST ## request method was not POST
        else:
            code = NO_DATA_GIVEN

    if code is not LOGIN_SUCCESS:
        ## error occured during login proc.
        return render(request,
                      "account/login.html",
                      addGlobalContext({'code': code,
                       "code_msg": login_get_code_msg(code),
                       'globals': config
                      }))
    else:
        return HttpResponseRedirect(request.GET.get("next",reverse("home")))


def logout_user(request):
    config.refresh()
    logout(request)
    return HttpResponseRedirect(reverse("home"))
    

def create_username(*args):
    config.refresh()
    import random
    vals = []
    for each in args:
        vals.append(smart_str(each))
    return "".join(vals)

@login_required(login_url="/login")
def addMemberWithArgs(request,created):
    config.refresh()
    form = CreateMemberForm()
    member = None
    if request.method == "POST":
        form = CreateMemberForm(request.POST)
        if form.is_valid():
            # the form is valid, so lets create the member
            data = form.cleaned_data
            if data['first_name'] == '' and data['last_name'] == '':
                created = False
            else:
                first_name =smart_str( data['first_name'].strip(" ").lower())
                last_name = smart_str(data['last_name'].strip(" ").lower())
                gender = smart_str(data['gender'].strip(' ').lower())
                ward_no = smart_str(data['ward_no'].strip(' ').lower())
                tole = smart_str(data['tole'].strip(' ').lower())
                city = smart_str(data['city'].strip(' ').lower())
                home_phone = smart_str(data['home_phone'].strip(' ').lower())
                parent_name = smart_str(data['parent_name'].strip(' ').lower())
                school_name = smart_str(data['school_name'].strip(' ').lower())
                school_class = smart_str(data['school_class'].strip(' ').lower())
                roll_no = smart_str(data['roll_no'].strip(' ').lower())
                date_of_birth = data['date_of_birth']

                ## creating the username
                username = create_username(first_name, last_name,ModUser.objects.all().count())
                member = ModUser.objects.create(
                        username=username
                        )
                if first_name not in ['']:
                    member.first_name = first_name
                if last_name not in ['']:
                    member.last_name = last_name
                if gender not in ['']:
                    member.gender = gender
                if ward_no not in ['']:
                    member.addr_ward_no = ward_no
                if tole not in ['']:
                    member.addr_tole = tole
                if city not in ['']:
                    member.addr_municipality = city
                if home_phone not in ['']:
                    member.telephone_home = home_phone
                if parent_name not in ['']:
                    member.parent_name = parent_name
                if school_name not in ['']:
                    member.school_name = school_name
                if school_class not in ['']:
                    member.school_class = school_class
                if roll_no not in ['']:
                    member.school_roll_no = roll_no
                if date_of_birth not in ['']:
                    member.date_of_birth = date_of_birth
                ## school_number and telephone_mobile are not added
                member.groups.add(Group.objects.get(name="Member"))
                member.save()
                created = True
                print "member created with username %s" % member

                return HttpResponseRedirect(reverse("addMemberWithArgs", kwargs=addGlobalContext({"member_created": created,"member": member})))
            
    return  render(request,
            "account/create_member.html",
            context=addGlobalContext(
                {
                    "form": form,
                    "member_created": created,
                    "member": ModUser.objects.order_by("-date_joined")[0]
                })
                )

@login_required(login_url="/login/")
def addMember(request):
    config.refresh()
    return addMemberWithArgs(request,created=False)

