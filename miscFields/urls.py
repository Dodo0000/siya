# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^$', 'miscFields.views.home',name="miscFieldsHome"),
        ]