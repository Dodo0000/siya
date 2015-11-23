from django.db import models
from django.utils.encoding import smart_str

from account.models import ModUser
# Create your models here.


class Individual(models.Model):
    user = models.OneToOneField(ModUser)

    primary_color = models.CharField(max_length=6,null=True)
    accent_color = models.CharField(max_length=6,null=True)

    def __str__(self):
        return self.user.get_name()



class Organization(models.Model):
    name = models.CharField(max_length=255, default="My Awesome Library")
    motto = models.TextField(null=True)
    members = models.ManyToManyField(Individual)

    no_of_books_at_once = models.IntegerField(default=2)
    no_of_days_to_borrow = models.IntegerField(default=10)
    rate_of_late_fees = models.FloatField(default=2)    ## price per day

    primary_color = models.CharField(max_length=6,default="1c6585")
    accent_color = models.CharField(max_length=6,default="eeeeee")
    

    def get_name(self):
        return smart_str(self.name)

    def get_short_name(self):
        return smart_str("".join([_[0] for _ in self.get_name().split(" ")]))

    def get_motto(self):
        return smart_str(self.motto)

    def get_primary_color(self):
        return self.primary_color

    def get_accent_color(self):
        return self.accent_color


    def deduce_primary_color(self,user):
        try:
            member = individual.objects.get(user)
        except :
            return self.primary_color

    @classmethod
    def get_no_of_instances(this):
        return len(this.objects.all())

    def __str__(self):
        return smart_str(self.name)
