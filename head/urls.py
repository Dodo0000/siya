# -*- coding: utf-8 -*-

from django.conf.urls import url

urlpatterns = [
    url(r'^dashboard/$', 'head.views.dashboard', name="dashboard"),
    url(r'^entry/$', 'head.views.entry', name="entry"),
    url(r'^entry/(?P<id>[0-9]+)$', 'head.views.editEntry', name="editEntry"),
    url(r'^book/(?P<id>[0-9]+)/$', 'head.views.bookInfo', name='book'),
    url(r'^book/validate$', 'head.views.validate_book', name='validate_book'),
    url(r'^book/add$', 'head.views.add_book', name="add_book"),
    url(r'^book/discard/confirm/(?P<id>[0-9]+)/$', 'head.views.deleteBookConfirm', name="delete_book_confirm"),
    url(r'^book/discard/(?P<id>[0-9]+)/$', 'head.views.deleteBook', name="delete_book"),
    url(r'^book/revive/(?P<id>[0-9]+)/$', 'head.views.reviveBook', name="revive_book"),
    url(r'^book/borrow/$', 'head.views.borrow', name='lend-book'),
    url(r'^book/borrow/(?P<username>.+)$', 'head.views.borrow_with_username', name='lend-book-with-username'),
    url(r'^book/borrow/(?P<acc_no>[0-9]+)$', 'head.views.borrow_with_acc_no', name='lend-book-with-acc_no'),
    url(r'^book/copy/(?P<old_acc>[0-9]+)/(?P<new_acc>[0-9]+)$', 'head.views.copyBook', name='copy-book'),
    url(r'^book/return/check/$', 'head.views.return_check_fees', name='return-book'),
    url(r'^report/$', 'head.views.report', name='report'),
    url(r'^about/library$', 'head.views.about', name='about-library'),
    url(r'^search/book/$', 'head.views.searchBook', name='search-book'),
        ]
