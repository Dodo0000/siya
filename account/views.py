from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout

from .models import ModUser
from head.models import Book, Lend
from head.views import home
from settings.models  import addGlobalContext

from settings.models import Globals

import datetime
# Create your views here.

@login_required(login_url="/login")
def profile(request, username):
    user = get_object_or_404(ModUser,username=username)
    books_borrowed = Lend.objects.filter(user=user,returned=False)
    len_books_borrowed = len(books_borrowed)
    return render(request, 'account/user.html', {'globals': Globals,'date': datetime.date.today(), 'search_user': user, 'books_borrowed': books_borrowed, 'len_books_borrowed': len_books_borrowed })



@login_required(login_url="/login")
def search_member(request):
    username = request.GET.get("username", None)
    if username is not None:
        user = ModUser.objects.filter(username=username)
        if len(user) == 1:
            user = user[0]
            return HttpResponseRedirect(reverse('profile', kwargs={"username":user.username}))
        else:
            return render(request, 'account/search_user.html', {'not_found': True, 'username': username, 'globals': Globals, 'date': datetime.date.today()})
    else:
        return render(request, 'account/search_user.html', {"globals": Globals, 'date': datetime.date.today()})



def login_get_code_msg(code):
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
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)


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
        if request.POST.get('username', None) is not None and request.POST.get("password", None) is not None:
            code = METHOD_NOT_POST ## request method was not POST
        else:
            code = NO_DATA_GIVEN

    if code is not LOGIN_SUCCESS:
        ## error occured during login proc.
        return render(request,
                      "account/login.html",
                      {'code': code,
                       "code_msg": login_get_code_msg(code),
                       'globals': Globals
                      })
    else:
        return HttpResponseRedirect(request.GET.get("next",reverse("home")))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))
    

def addMember(request):
    fields = (
                ("First Name","first_name"),
                ("Last Name", "last_name"),
                ("Gender", "gender"),
                ("Ward No.", "ward_no"),
                ("Tole", "tole"),
                ("City", "city"),
                ("Home Phone No.", "home_phone"),
                ("Parent's Name", "parent_name"),
                ("Parent's Phone No.", "Parent's Phone No."),
                ("School Name", "school_name"),
                ("School Telephone", "school_phone"),
                ("Class", "school_class"),
                ("Roll No.", "roll_no"),
                ("Date Of Birth","date_of_birth"),
            )
    render(request, "accounts/addMember.html", addGlobalContext({"fields": fields}))
