from django.shortcuts import render

from settings.models import Globals
from ledger.models import OneDaysEntry

from datetime import datetime
# Create your views here.


def journalHomeArgs(request,addCreditSuccess=False,addDebitSuccess=False):
    '''
    journalHome with extra arguments
    '''
    context = {
            'globals': Globals,
            'date': datetime.today(),
            'dayEntries': OneDaysEntry.objects.all(),
            }

    context.update(
            [
                ["creditSuccess",addCreditSuccess],
                ["debitSuccess",addDebitSuccess]
            ])

    return render(request,'ledger/journalHome.html',context)


def journalHome(request):
    return journalHomeArgs(request)


def addCredit(request):
    if request.GET.get("id", None)== None:
        pass
