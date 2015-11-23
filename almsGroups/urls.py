
from django.conf.urls import patterns, url

urlpatterns = [
            url(r'^(?P<group_added>[01]+)/(?P<group_name>[a-zA-Z0-9_]+)/$', 'almsGroups.views.homeWithArgs',name="almsGroupsHomeWithArgs"),
            url(r'^$', 'almsGroups.views.home',name="almsGroupsHome"),
            url(r'^add/$', 'almsGroups.views.addGroup',name="addNewGroup"),
        ]
