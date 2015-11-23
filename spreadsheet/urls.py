

from django.conf.urls import include, url


urlpatterns = [
            url(r'^allauthors/$', 'spreadsheet.views.getAllAuthorData',name="spreadsheetGetAllAuthorData"),
            url(r'^allbooks/$', 'spreadsheet.views.getAllBookData',name="spreadsheetGetAllBookData"),
            url(r'^allpublishers/$', 'spreadsheet.views.getAllPublisherData',name="spreadsheetGetAllPublisherData"),
            url(r'^booksWithoutCallNumber/$', 'spreadsheet.views.getBooksWithoutCallNumber',name="spreadsheetBooksWithoutCallNumber"),
        ]
