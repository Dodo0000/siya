from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^journal/$', 'ledger.views.journalHome',name='journalHome'),
            url(r'^addCredit/$', 'ledger.views.addCredit',name='addCredit'),
        ]
