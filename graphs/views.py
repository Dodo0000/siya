from django.shortcuts import render
import datetime
from django.http import HttpResponse
import pygal
from head.models import BookSaver
# Create your views here.

def getMonthlyBooksSavedGraph(request, username):
    if request.user.is_staff:
	    books_saved = BookSaver.objects.filter(user__username=username)
	    dates = set()
	    x = set()
	    for _ in books_saved:
		dates.add(_.date)
	    for _ in dates:
		x.add(datetime.date(_.year, _.month, 1))
	    x = sorted(x)
	    dataset = [(_,books_saved.filter(date__year=_.year,date__month=_.month).count()) for _ in x]
	    dateline = pygal.DateLine(x_label_rotation=90)
	    dateline.x_labels = x
	    dateline.add("Books Saved for Each Month", dataset)
	    return dateline.render_django_response()
    else:
        return HttpResponse("")
    

