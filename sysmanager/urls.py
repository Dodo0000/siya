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
    url(r'^book/(?P<accNo>[0-9]+)/$', 'head.views.bookInfo',name='book'),
    url(r'^user/(?P<username>[a-z]+)/$', 'account.views.profile', name='profile'),
    url(r'^book/borrow/$', 'head.views.borrow', name='lend-book'),
    url(r'^book/return/check/$', 'head.views.return_check_fees', name='return-book'),
    url(r'^report/$', 'head.views.report', name='report'),
    url(r'^search/book/$', 'head.views.searchBook', name='search-book'),
    url(r'^search/member/$', 'account.views.search_member', name="search-member"),
    url(r'^login/$', 'account.views.login_user', name="login"),
    url(r'^logout/', 'account.views.logout_user', name="logout"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^entry/$', 'head.views.entry', name="entry"),
    url(r'^book/validate$','head.views.validate_book',name='validate_book'),
    url(r'^book/add$', 'head.views.add_book', name="add_book"),
    url(r'^book/discard/confirm/(?P<accNo>[0-9]+)/$', 'head.views.deleteBookConfirm', name="delete_book_confirm"),
    url(r'^book/discard/(?P<accNo>[0-9]+)/$', 'head.views.deleteBook', name="delete_book"),
]
