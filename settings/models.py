from django.db import models

import datetime

from configs.models import Organization as configsOrganization

class Global:
    '''
    this is a wrapper arpund the configs.models.Organization class
    to support the Globals class data structure.
    '''
    ## somthing to fix ^





class Globals:

    books={

        'columns': [
            ('Call Number', 0.5, "call_no"),
            ('Authors', 0.9, "auth"),
            ('Title', 1, "title"),
            ('Published Place', 1, 'pub_place'),
            ('Publisher Name', 1, "pub_name"),
            ('Published Year', 0.5, 'pub_year'),
            ("No. Of Pages", 0.5, "no_of_pages"),
            ("Price", 0.5, 'price'),
            ('Series', 0.5, 'ser'),
            ("ISBN", 1, "isbn"),
            ('Edition', 0.5, 'edtn'),
            ("volume", 0.5, 'vol'),
            ('Accession Number', 1, "acc_no"),
            ('Subject & Keywords', 1, "kwds"),
            ("Gifted By", 1, "gftd_name"),
            ("Doner's Phone Number", 1, "gftd_phn"),
            ("Donor's Email", 1, "gftd_email")
        ],
        "borrow":{
            "max_days":10,
            "max_books":2
        }
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
    if context.__class__ == dict:
        return context.update(global_dict)
    elif context == None:
        return global_dict
    else:
        raise TypeError("context is not a dictionary")
