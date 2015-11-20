
from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^$', 'almsGroups.views.home',name="almsGroupsHome"),
            url(r'^add/$', 'almsGroups.views.addGroup',name="addNewGroup"),
        ]
