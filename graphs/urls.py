# -*- coding: utf-8 -*-

from django.conf.urls import url

urlpatterns = [
    url(r'^savedBooks/(?P<username>.+)/$',
        'graphs.views.getMonthlyBooksSavedGraph',
        name='graphGetMonthlyBooksSavedGraph'),
        ]
