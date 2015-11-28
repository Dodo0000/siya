from django import forms
from django.forms import ModelForm
from account.models import ModUser
from django.contrib.admin import widgets

class CreateMemberForm(forms.Form):
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    gender = forms.ChoiceField(label="Gender",choices=(("male","male"),("female","female")))
    ward_no = forms.CharField(label="Ward No.")
    tole = forms.CharField(label="Tole")
    city = forms.CharField(label="City")
    home_phone = forms.CharField(label="Home Phone No.")
    parent_name = forms.CharField(label="Parent's Name")
    school_name = forms.CharField(label="School Name")
    school_class = forms.CharField(label="Class")
    roll_no = forms.CharField(label="Roll No.")
    date_of_birth = forms.DateTimeField(widget=widgets.AdminDateWidget(),label="Date Of Birth")

