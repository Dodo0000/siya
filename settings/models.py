from django.db import models

import datetime

from configs.models import Organization as configsOrganization

from django.conf import settings
import os

class Globals:
    '''
    this is a wrapper arpund the configs.models.Organization class
    to support the Globals class data structure.
    '''
    def __init__(self):
        import configparser
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(settings.BASE_DIR, "config.ini"))
        self.books = self.config['books']
        self.books_columns = self.config['columns']
        self.yalms = self.config['alms']
        self.misc = self.config['misc']

    def load(self):
        import configparser
        self.config.read(os.path.join(settings.BASE_DIR, "config.ini"))

    def add(self,key, value):
        self.config[key] = value
        self.save()
        self.load()

    def save(self):
        with open(os.path.join(settings.BASE_DIR, "config.ini")) as configfile:
            self.config.write(configfile)




'''
class Globals:

    books={
        "borrow_max_days":10,
        "borrow_max_books":2
    }
    columns = {
            'Call Number' : "call_no",
            'Authors' : "auth",
            'Call Number' : "call_no",
            'Published Place' : 'pub_place',
            'Publisher Name' : "pub_name",
            "Price" : 'price',
            'Series' : 'ser',
            "ISBN" : "isbn",
            'Edition' : 'edtn',
            "volume" : 'vol',
            'Accession Number' : "acc_no",
            'Subject & Keywords' : "kwds",
            "Gifted By" : "gftd_name",
            "Doner's Phone Number" : "gftd_phn",
            "Donor's Email" : "gftd_email",
            }
    late_fees_price = 2 #rs per day
    late_fees_rate = late_fees_price

    report = {
        "time_period": 3 ## months
    }

    yalms = {
        "sft_short_name": "yalms",
        "sft_long_name": "Yet Another Library Management Software",
        "org_long_name": "Nepal Japan Children Library",
        "org_short_name": "NJCL",
        "org_motto": "Reading Is Fun!",
    }
'''

class AccessionNumberCount(models.Model):
    accession_number = models.IntegerField(default=0)

    @staticmethod
    def add1():
        acc_nos = AccessionNumberCount.objects.all()
        if len(acc_nos) == 1:
            acc_nos[0].accession_number += 1 
            acc_nos[0].save()
            return 0
        else:
            return 1

    @staticmethod
    def get_no():
        acc_nos = AccessionNumberCount.objects.all()
        if len(acc_nos) == 1:
            return acc_nos[0].accession_number
        else:
            return 0

def addGlobalContext(context=None):
    global_dict = {
                "globals": Globals,
                "date": datetime.date.today()
            }
    if context != None and context.__class__ == dict:
        context.update(global_dict)
        return context
    elif context == None:
        return global_dict
    else:
        raise TypeError("context is not a dictionary")
