# -*- coding: utf-8 -*-
"""sysmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'head.views.home', name='home'),
    url(r'^dashboard/$', 'head.views.dashboard', name='dashboard'),
    url(r'^entry/$', 'head.views.entry', name="entry"),
    url(r'^entry/(?P<acc_no>[0-9]+)$', 'head.views.editEntry', name="editEntry"),
    url(r'^book/(?P<accNo>[0-9]+)/$', 'head.views.bookInfo',name='book'),
    url(r'^book/validate$','head.views.validate_book',name='validate_book'),
    url(r'^book/add$', 'head.views.add_book', name="add_book"),
    url(r'^book/discard/confirm/(?P<accNo>[0-9]+)/$', 'head.views.deleteBookConfirm', name="delete_book_confirm"),
    url(r'^book/discard/(?P<accNo>[0-9]+)/$', 'head.views.deleteBook', name="delete_book"),
    url(r'^book/revive/(?P<accNo>[0-9]+)/$', 'head.views.reviveBook', name="revive_book"),
    url(r'^book/borrow/$', 'head.views.borrow', name='lend-book'),
    url(r'^book/copy/(?P<old_acc>[0-9]+)/(?P<new_acc>[0-9]+)$', 'head.views.copyBook', name='copy-book'),
    url(r'^book/return/check/$', 'head.views.return_check_fees', name='return-book'),
    url(r'^report/$', 'head.views.report', name='report'),
    url(r'^search/book/$', 'head.views.searchBook', name='search-book'),
    url(r'^search/member/$', 'account.views.search_member', name="search-member"),
    url(r'^login/$', 'account.views.login_user', name="login"),
    url(r'^register/person/$', 'account.views.addWorker', name="addWorker"),
    url(r'^register/person/new/(?P<created>.*)$', 'account.views.addWorkerWithArgs', name="addWorkerWithArgs"),
    url(r'^register/member/$', 'account.views.addMember', name="addMember"),
    url(r'^register/member/new/(?P<created>.*)$', 'account.views.addMemberWithArgs', name="addMemberWithArgs"),
    url(r'^logout/', 'account.views.logout_user', name="logout"),
    url(r'^user/(?P<username>.+)/$', 'account.views.profile', name='profile'),
    url(r'^verifySchool/(?P<userName>.+)/$', 'account.views.verifySchool', name='verifySchool'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('ledger.urls')),
    url(r'^groups/', include('almsGroups.urls')),
    url(r'^booktool/', include('booktool.urls')),
    url(r'^spreadsheet/', include('spreadsheet.urls')),
    url(r'^rst/', include('restructuredText.urls')),
    url(r'^miscfields/', include('miscFields.urls')),
    url(r'^settings/', include('settings.urls')),
]
