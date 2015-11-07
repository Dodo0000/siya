from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^journal/$', 'ledger.views.journalHome',name='journalHome'),
            url(r'^addCredit/$', 'ledger.views.addCredit',name='addCredit'),
            url(r'^addDebit/$', 'ledger.views.addDebit',name='addDebit'),
            url(r'^addEntry/$', 'ledger.views.addOneDaysEntry',name='addOneDaysEntry'),
        ]
