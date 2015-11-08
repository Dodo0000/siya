from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager, Group
from django.db import models
from django.utils import timezone
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse


import datetime

# Create your models here.

class UserType(models.Model):
    '''
    This class describes the type of user
    The types of users are: 
        * member
        * volunteer
        * managers
    '''
    _type = models.CharField(max_length=20)
    slug = models.SlugField()

    def type(self):
        return self._type

    def __str__(self):
        return self._type


class UserManager(BaseUserManager):

    '''
    Dont grant this user staff access!!
    '''
    def create(self, username, user_type, super_user=False, first_name=None, last_name=None, password=None, **extra_fields):
        if not username:
            raise ValueError("Email is required to create User")

        user = self.model(username=username,
                first_name=first_name,
                last_name=last_name,
                user_type=user_type,
                **extra_fields
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, user_type=None):
        if not username:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not user_type:
            user_type= UserType.objects.get_or_create(_type="member",slug="member")[0]

        user = self.create(username=username, password=password,super_user=True, user_type=user_type)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

    def add(self, user):
        self.viewers.add(user.viewer)

class ModUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=90,null=True)
    last_name = models.CharField(max_length=90,null=True)
    username = models.CharField(max_length=25, unique=True)

    date_joined = models.DateTimeField('Date Joined',default=timezone.now)

    sex = models.CharField(max_length=6,
            null=True,
            choices=(
                ('male','male'),
                ('female','female'),
                ))

    addr_ward_no = models.CharField(max_length=20, null=True)
    addr_tole = models.CharField(max_length=100, null=True)
    addr_municipality = models.CharField(max_length=100, null=True)

    telephone_home = models.IntegerField(null=True)
    telephone_mobile = models.IntegerField(null=True)

    parent_name = models.CharField(max_length=255,null=True)
    parent_telephone_number = models.IntegerField(null=True)

    school_name = models.CharField(max_length=255,null=True)
    school_telephone = models.IntegerField(null=True)
    school_class = models.CharField(max_length=5,null=True)
    school_roll_no = models.CharField(max_length=3,null=True)
    school_varified = models.NullBooleanField(default=False)
    
    date_of_birth = models.DateField(null=True)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def get_address(self):
        return "{0} ward, {1}, {2}".format(self.addr_ward_no, self.addr_tole, self.addr_municipality)

    def get_telephone(self):
        return "home: {0}, mobile: {1}, parent's: {2}".format(self.telephone_home, self.telephone_mobile, self.parent_telephone_number)
    
    def get_age(self):
        return datetime.date.today().year - self.date_of_birth.year

    
    def save(self,commit=True,create_new=False, *args, **kwargs):
        if not self.is_active:
            self.send_email_activation_confirmation()
        if commit:
            super(ModUser, self).save(*args,**kwargs)

    def is_male(self):
        return self.sex == "male"
    
    def is_female(self):
        return self.sex == "female"
            
    def get_short_name(self):
        if self.first_name is None:
            return self.username
        else:
            return self.first_name

    def get_name(self):
        if self.first_name is None or self.last_name is None:
            return self.username
        return "{0} {1}".format(self.first_name, self.last_name).title()



    def get_all_attr(self):
        return [
            ('Name', self.get_name()),
            ("Username", self.username),
            ("Gender", self.sex),
            ("Age", self.get_age()),
            ("Parent's Name", self.parent_name),
            ("Phone Number", self.get_telephone()),
            ("School Name", self.school_name),
            ("Class", self.school_class),
            ("Roll No.", self.school_roll_no),
            ("School Phone Number", self.school_telephone),
        ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.get_name()