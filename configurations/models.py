from django.db import models
from django.utils.encoding import smart_str

from accounts.models import ModUser
# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=255, default="My Awesome Library")
    motto = models.TextField(null=True)
    members = models.ManyToManyField(ModUser)

    no_of_books_at_once = models.IntegerField(default=2)
    no_of_days_to_borrow = models.IntegerField(default=10)
    rate_of_late_fees = models.FloatField(default=2)    ## price per day

     
    

    def get_name(self):
        return smart_str(self.name)

    def get_short_name(self):
        return smart_str("".join([_[0] for _ in self.get_name().split(" ")]))

    def get_motto(self):
        return smart_str(self.motto)

    @classmethod
    def get_no_of_instances(this):
        return len(this.objects.all())

    def __str__(self):
        return smart_str(self.name)
