'''
 ___  __                                      
|_ _|/ _|  _   _  ___  _   _    __ _ _ __ ___ 
 | || |_  | | | |/ _ \| | | |  / _` | '__/ _ \
 | ||  _| | |_| | (_) | |_| | | (_| | | |  __/
|___|_|    \__, |\___/ \__,_|  \__,_|_|  \___|
           |___/                              
                    _ _               _   _     _                           
 _ __ ___  __ _  __| (_)_ __   __ _  | |_| |__ (_)___     _   _  ___  _   _ 
| '__/ _ \/ _` |/ _` | | '_ \ / _` | | __| '_ \| / __|   | | | |/ _ \| | | |
| | |  __/ (_| | (_| | | | | | (_| | | |_| | | | \__ \_  | |_| | (_) | |_| |
|_|  \___|\__,_|\__,_|_|_| |_|\__, |  \__|_| |_|_|___( )  \__, |\___/ \__,_|
                              |___/                  |/   |___/             
 _                                     _ _  __      
| |__   __ ___   _____   _ __   ___   | (_)/ _| ___ 
| '_ \ / _` \ \ / / _ \ | '_ \ / _ \  | | | |_ / _ \
| | | | (_| |\ V /  __/ | | | | (_) | | | |  _|  __/
|_| |_|\__,_| \_/ \___| |_| |_|\___/  |_|_|_|  \___|
                                                    


If you can keep your head when all about you
 Are losing theirs and blaming it on you,
If you can trust yourself when all men doubt you,
  But make allowance for their doubting too;
If you can wait and not be tired by waiting,
  Or being lied about, don't deal in lies,
Or being hated, don't give way to hating,
  And yet don't look too good, nor talk too wise:

If you can dream-and not make dreams your master;
  If you can think-and not make thoughts your aim;
If you can meet with Triumph and Disaster
  And treat those two impostors just the same;
If you can bear to hear the truth you've spoken
  Twisted by knaves to make a trap for fools,
Or watch the things you gave your life to, broken,
  And stoop and build 'em up with worn-out tools:

If you can make one heap of all your winnings
  And risk it on one turn of pitch-and-toss,
And lose, and start again at your beginnings
  And never breathe a word about your loss;
If you can force your heart and nerve and sinew
  To serve your turn long after they are gone,
And so hold on when there is nothing in you
  Except the Will which says to them: "Hold on!"

If you can talk with crowds and keep your virtue,
  Or walk with Kings-nor lose the common touch,
If neither foes nor loving friends can hurt you,
  If all men count with you, but none too much;
If you can fill the unforgiving minute
  With sixty seconds' worth of distance run,
Yours is the Earth and everything that's in it,
  And-which is more-you'll be a Man, my son.

'''

from head.models import Book, Lend, Author, KeyWord, Publisher, Gifter
from account.models import ModUser
from settings.models import Globals, AccessionNumberCount

from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import datetime
import json

from fuzz.search import searchBookTitle, searchBookAuthor,searchBookKeywords

# Create your views here.

TYPES = [
    "Title",
    "Author",
    "Keyword",
    "Acc No",
    "Call No",
    "Publisher"
]

TIME_PERIOD = Globals.report['time_period']  #months

LATE_FEES_PRICE = Globals.late_fees_price #rupees per day
NO_DAYS_TO_BORROW_BOOK = Globals.books['borrow']['max_days'] # number of days for which a book is to be borrowed
MAX_NUM_OF_BOOKS_TO_BORROW = int(Globals.books['borrow']['max_books']) # max number of books member can borrow at once

NO_OF_BOOKS_PER_PAGE = 10

GLOBAL_CONTEXT = {
        "globals": Globals,
        "date": datetime.date.today()
        }

NP_NUM = {
        [
            ')',
            '!',
            '@',
            '#',
            '$',
            '%',
            '^',
            '&',
            '*',
            '('][x]: str(x)  for x in range(0,10)
        }



LANG_LIST = [
            'EN',
            'NP'
        ]

CURRENT_LANGUAGE = LANG_LIST[0]


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False



def toint(val,lang="EN"):
    if val is None or val == "None" or val == "":
        return 0
    else:
        if lang.upper() == "NP":
            l = ""
            for char in str(val):
                l += NP_NUM[str(char)]
            return int(l)
        elif lang.upper() == "EN":
            return int(val)
        else:
            return int(val)


##############################################################################
############################### AJAX CALL VIEWS ##############################

def validate_book(request):
    '''
    checks if book with the given accession number exists
    returns True if it does,
    false if it doesn't.
    '''
    acc_no = request.GET.get('accNo', None)
    if acc_no is None:
        return JsonResponse({"data_correct": False, "valid":False})
    is_valid = -1
    if acc_no is not None:
        is_valid = int(len(Book.objects.filter(accession_number=acc_no,state=0)) > 0)

    json_dict = {
                'data_correct': True,
                "exists":is_valid,
                "accNo": acc_no
            }

    return JsonResponse(json_dict)



def add_book(request):
    all_attrs = [_[2] for _ in Globals.books['columns']] + ["language"]
    each = dict()   ## store post data
    STATE = 0
    
    return HttpResponse(each)

    for _ in all_attrs:
        each[_] =  request.POST.get(_)
    CURRENT_LANGUAGE = request.POST.get("language", "EN")


    if "," in str(each['acc_no']):
        acc_list = [_.strip(" ") for _ in each['acc_no'].split(",")]
    elif "-" in str(each['acc_no']):
        acc_strip = [int(_) for _ in each['acc_no'].split("-")]
        if len(acc_strip) != 2:
            raise TypeError("Range Too Many or To Few (not 2) ")
        acc_list = list(range(acc_strip[0], acc_strip[1]+1))
    else:
        acc_list = [each['acc_no']]


    for val in acc_list:
        if val.__class__ == str:
            accession_number = val.strip(" ")
        else:
            accession_number = val


                    
        if accession_number in [None,"None", 0,"0",""] or "-" in accession_number:
            STATE = -1
            continue
        if each['no_of_pages'] in [None, "", 0, "0"] or '-' in each['no_of_pages']:
            STATE = -1
            continue
        if each['title'] in [None, "", 0, "0"]:
            STATE = -1
            continue

        # either create a new book or edit an already existing book
        try:
            book = Book.objects.get(accession_number=toint(accession_number))
        except DoesNotExist:
            book = Book.objects.create(accession_number=toint(accession_number),
                    title=each['title'],
                    no_of_pages=toint(
                        each['no_of_pages']))
        
        for author_name in each['auth'].split("%"):
            author_name = author_name.strip(" ")
            author = Author.objects.get_or_create(
                name=author_name,
                slug = slugify(author_name))
            if author[1]:
                author = author[0]
                author.save()
            else:
                author = author[0]
            book.author.add(author)

        if (
                each['pub_place'] is None or
                each['pub_year'] is None or
                each['pub_name'] is None
        ) is False:
            publisher = Publisher.objects.get_or_create(
                place=each['pub_place'],
                name=each['pub_name'],
                year=toint(each['pub_year']))
            if publisher[1]:
                publisher = publisher[0]
                publisher.save()
            else:
                publisher = publisher[0]
            book.publisher = publisher

        book.call_number = each['call_no']

        if (each['ser'] is None) is False:
            book.series = each['ser']

        if (each['edtn'] is None) is False:
            book.edition = each['edtn']


        if (each['isbn'] is None) is False:
            book.isbn = each['isbn']

        if (each['price'] is None) is False:
            book.price = each['price']
        
        if (each['gftd_name'] is None) is False:
            gifter_name = each['gftd_name']
            gifter_phn = each['gftd_phn']
            gifter_email = each['gftd_email']
            gifter = Gifter.objects.get_or_create(
                        gifter_name=gifter_name,
                    )
            gifter = gifter[0]
            if gifter_phn != "" and gifter_phn.isdigit():
                gifter.phone = gifter_phn
            if gifter_email != "" and validateEmail(gifter_email):
                gifter.email = email
            gifter.save()
            book.gifted_by = gifter

        if each['vol'] != None and each['vol'] != "None":
            if each['vol'].isdigit() == True:
                book.volume = int(each['vol'])
            else:
                book.volume = acc_list.index(val) + 1
        else:
            book.volume = acc_list.index(val) + 1

        for keyword in each['kwds'].split(","):
            keyword = keyword.strip(' ')
            kw = KeyWord.objects.get_or_create(name=keyword,slug=slugify(keyword))
            if kw[1]:
                kw = kw[0]
                kw.save()
            else:
                kw = kw[0]
            book.keywords.add(kw)
        book.save()
        AccessionNumberCount.add1()
        STATE = 0
    if STATE == 0:
        return JsonResponse({"success": True,'acc_no': AccessionNumberCount.get_no()})
    else:
        return JsonResponse({"success": False,'acc_no': AccessionNumberCount.get_no()})

'''
def add_book(request):
    all_attrs = [_[2] for _ in Globals.books['columns']]
    required_attrs = all_attrs[:3]
    optional_attrs = all_attrs[3:]

    if len(
            [
                1 for each in required_attrs
                if request.POST.get(each, None) is None
            ]
           ) != 0:
        return JsonResponse({"exists": False, "success": False, "reason_failure": "all necessary attrs not found " + str(request.GET.get('no_of_pages', "NULL"))})
   
    attr_values = {each:request.POST.get(each, None) for each in all_attrs}

    
    #check if book exists brefore creating it
    if (len(Book.objects.filter(
                accession_number=attr_values['acc_no']
                )
            ) > 0 ) is True:
        return JsonResponse({"exists": False, success:False, "reason_failure": "book does not exist"})
    
    if "," in attr_values['acc_no']:
        acc_list = [_.strip(' ') for _ in attr_values['acc_no'].split(",")]
    elif "-" in attr_values['acc_no']:
        acc_strip = [int(_) for _ in attr_values['acc_no'].split("-")]
        if len(acc_strip) != 2:
            raise TypeError("Range Too Many or Too Few(not 2)")
        acc_list = list(range(acc_strip[0],acc_strip[1]+1))
    else:
        acc_list = [attr_values['acc_no']]

    for each in acc_list:

        book = Book.objects.get_or_create(
                accession_number=each,
                title=attr_values['title'],
                no_of_pages=toint(attr_values['no_of_pages'])
                )

        if book[1] == True:
            continue

        #book.call_number = attr_values['call_no']
        book.call_number = "attr_values"

        authors = attr_values['auth'].split("%")
        for name in authors:
            if name != "":
                author = Author.objects.get_or_create(
                        name=name,
                        slug=slugify(name))
                book.author.add(author[0])
                author[0].save()

        if len([
            attr_values[_] is None 
            for _ in [
                'pub_name',
                'pub_place',
                'pub_year'
                ]]) > 0:
                pass #### value of publisher_* wasn't given
        else:
            publisher = Publisher.objects.get_or_create(
                    name=attr_values['publisher_name'],
                    place=attr_values['publisher_place'],
                    year=attr_values['publisher_year'])
            Book.publisher = publisher[0]
            publisher[0].save()

        book.series = attr_values['ser']

        book.edition = attr_values['edtn']

        book.price = attr_values['price']

        book.volume = attr_values['vol']

        kwds = attr_values['kwds'].split(",")
        for each in kwds:
            kwrd = KeyWord.objects.get_or_create(name=each,slug=slugify(each))
            book.keywords.add(kwrd[0])
            kwrd[0].save()

        ## add all attributes to book before saving it.
        book.save()


    return JsonResponse({"call_no": book.call_number,"success":  True})
'''



        


##############################################################################




@login_required(login_url="/login")
def editEntry(request,acc_no):
    if acc_no != None:
        books = Book.objects.filter(accession_number=acc_no)
        if len(books) < 1:
            return HttpResponseRedirect(reverse("entry"))
        else:
            book = books[0]
        clear_fields = False
    else:
        book = None
        clear_fields = True
    total_entry_space = 12
    
    columns_for_table =  list(enumerate(Globals.books['columns'], 1))
    columns_for_entry = list(enumerate(( _[1] for _ in columns_for_table),1 ))
    
    columns_for_entry_div = [ columns_for_entry[c:c+2] for c in range(0,len(columns_for_entry)+1,2)]

    total_no_of_cols_table = len(columns_for_table)
    total_no_of_cols_entry = len(columns_for_entry)

    if total_no_of_cols_entry <= 12:
        div_len = 12 / total_no_of_cols_entry
        div_offset = (12 - (div_len * total_no_of_cols_entry)) / 2
    else:
        div_len = total_no_of_cols_entry / 12
        div_offset = ((div_len * total_no_of_cols_entry) - 12) / 2

    
    return render(request,
                  "head/entry.html", {
                      'globals': Globals,
                      'date': datetime.date.today(),
                      "columns_for_table": columns_for_table,
                      "columns_for_entry": columns_for_entry,
                      "columns_for_entry_div": columns_for_entry_div,
                      'div_len': div_len,
                      'book': book,
                      'div_offset': div_offset,
                      'total_columns_table': total_no_of_cols_table,
                      'total_columns_entry': total_no_of_cols_entry,
                      'columns_entry_json': json.dumps(columns_for_entry, indent=4),
                      'columns_table_json': json.dumps(columns_for_table, indent=4),
                      'largest_accession_number': AccessionNumberCount.get_no(),
                      'clear_fields': int(clear_fields)
                  })


@login_required(login_url="/login/")
def entry(request):
    return editEntry(request,None)


@login_required(login_url="/login")
def report(request):
    no_of_months = TIME_PERIOD
    this_date = datetime.date.today()
    start_month =  this_date.month - no_of_months
    if start_month < 0:
        start_date = datetime.date(this_date.year - 1, 12 - start_month, this.day)
    else:
        start_date = datetime.date(this_date.year, start_month, this_date.day)
    time_period = this_date - start_date

    books_cataloged_in_tp = Book.objects.exclude(
        accessioned_date__gte=this_date,state=0).filter(
            accessioned_date__gte=start_date)

    books_cataloged_until_tp = Book.objects.exclude(
        accessioned_date__gte=start_date
    )

    members_added_in_tp = ModUser.objects.exclude(
        date_joined__gte=this_date
    ).filter(
        date_joined__gte=start_date
    )

    members_added_until_tp = ModUser.objects.exclude(
        date_joined__gte=start_date
    )

    return render(request,
                  "head/report.html",
                  {'globals':Globals,
                   'date': datetime.date.today(),
                   'this_date': this_date,
                   'start_date': start_date,
                   'time_period': time_period.days/30,
                   'books_cataloged_in_tp': books_cataloged_in_tp,
                   'books_cataloged_until_tp': books_cataloged_until_tp,
                   'members_added_in_tp': members_added_in_tp,
                   'members_added_until_tp': members_added_until_tp
                  })


def home(request):
    return render(request, 'head/home.html', {'globals':Globals, 'date': datetime.date.today()})



@login_required(login_url="/login")
def dashboard(request):
    logged_in = request.META.get('logged_in', None)
    today = datetime.date.today()
    if today.month - TIME_PERIOD < 0:
        start_date = datetime.date(today.year - 1, 12 - today.month + TIME_PERIOD, today.day)
    else:
        start_date = datetime.date(today.year, today.month - TIME_PERIOD, today.day)

    ## problem, the _gte filter with `today' excludes the data entered on today...fix this
    time_period = today - start_date
    members_added_during_tp = ModUser.objects.exclude(
            date_joined__gte=today).filter(date_joined__gte=start_date)
    total_members = ModUser.objects.all()
    books_cataloged_during_tp = Book.objects.exclude(
            accessioned_date__gte=today).filter(accessioned_date__gte =start_date,state=0)
    recently_added_books =  list(Book.objects.filter(state=0,accessioned_date=datetime.date.today()).order_by("-accessioned_date"))
    recently_added_books.reverse()
    total_books = Book.objects.all()
        
    return render(request, "head/dashboard.html", {
        'globals':Globals,
        "members_added_during_tp": members_added_during_tp,
        "members_added_before_tp": total_members.exclude(date_joined__gte=start_date),
        'total_members': total_members,
        'books_cataloged_during_tp': books_cataloged_during_tp,
        'books_cataloged_before_tp': total_books.exclude(accessioned_date__gte=start_date),
        'total_books': total_books,
        'types': TYPES,
        'time_period': time_period.days / 30,
        'start_date': start_date,
        'recently_added_books': recently_added_books,
        'recently_added_members': ModUser.objects.order_by("-date_joined"),
        'date': today,
        'logged_in': logged_in
    })



@login_required(login_url="/login")
def deleteBookConfirm(request,accNo):
    if accNo.isdigit():
        book = Book.objects.filter(accession_number=accNo,state=0)
        if len(book) == 0 or len(book) > 1:
            context_dict = {
                    "state": -1, 
                    "message": "The No. of  book With Accession Number `{}` Was not 1".format(accNo),
                    }
        else:
            context_dict = {
                    "state": 0,
                    "message": "Are You Sure You want to delete this Book?",
                    "book": book[0]
                    }
    else:
        context_dict = {
                "state": -1,
                "message": "The Accession Number `{}` Is Invalid".format(accNo)
                }

    context_dict.update(GLOBAL_CONTEXT)
    return render(request, "head/delete_book.html", context_dict)

@login_required(login_url="/login")
def deleteBook(request,accNo):
    book = Book.objects.get(accession_number=accNo)
    book.discard()
    context_dict = {"book":book}
    context_dict.update(GLOBAL_CONTEXT)
    return render(request, "head/deleted_book.html", context_dict)


def searchBook(request):

    value = request.GET.get("search", None)
    type_ = request.GET.get("type", None)
    booklist = []
    '''
    Search algorithm : 
    Step 1 : Check if the query matches any books as a whole
    Step 2a : Check if each word in the query matches a book
    Step 2b : If each word matches queries then find the queries which match all the words
              in the query
    Step 2c : If no book matches all the words in the book then find the book(s) which matches
              most of the words in the query
    < Note : In Step 2c, meaning the word "most" is very flexible. >
    '''
    page = request.GET.get("page", 1)
    all_books = Book.objects.all()

    if value is not None:
        value = value.split(" ")
        if type_ in TYPES:
            if type_ == "Title":
                books = searchBookTitle(" ".join(value), all_books)
            elif type_ == "Call No":
                books = Book.objects.filter(call_number__contains=value[0]).order_by("call_number")
            elif type_ == "Acc No":
                books = Book.objects.filter(accession_number__contains=value[0]).order_by("-accession_number")

            elif type_ == "Keyword":
                books = searchBookKeywords(" ".join(value), all_books)
            elif type_ == "Publisher":
                books = Book.objects.filter(publisher__name__contains=value[0]).order_by("publisher__name")
                for each in value[1:]:
                    bookf = books.filter(publisher__name__contains=each).order_by("publisher__name")
                    if len(bookf) > 0:
                        books = bookf
                    else:
                        break
            elif type_ == "Author":
                books = searchBookAuthor(" ".join(value), all_books)
        booklist = books
        if len(booklist) == 0:
            not_found = True
        else:
            not_found = False

    else:
        value = []
        not_found = None

    paginator = Paginator(booklist, NO_OF_BOOKS_PER_PAGE)
    try:
        booklist = paginator.page(page)
    except PageNotAnInteger:
        booklist = paginator.page(1)
    except EmptyPage:
        booklist = paginator.page(paginator.num_pages)
    return render(request,
                  "head/search_books.html",
                  {
                      'globals': Globals,
                      'total_books_len': len(all_books),
                      'date': datetime.date.today(),
                      "books": booklist,
                      "book_pages": list(range(1, paginator.num_pages+1)),
                      "value": " ".join(value),
                      "type": type_,
                      "types": TYPES,
                      "not_found": not_found
                  })




def bookInfo(request, accNo):
    books = Book.objects.filter(accession_number=accNo)
    if len(books) == 0:
        return HttpResponse("Book Not Found")
    else:
        book = books[0]

    lends =  Lend.objects.filter(book=book)
    if_borrowed = False
    
    if len(lends) == 1:
        lends = lends[0]
        days_ago = datetime.date.today() - lends.lending_date
        is_borrowed = True
        if days_ago.days == 0:
            days_ago = "today"
        else:
            days_ago = str(days_ago.days) + " days ago"
    else:
        is_borrowed = False
        lends = None
        days_ago = None

    if lends != None:
        late_fees = lends.get_late_fees()
    else:
        late_fees = 0

    return render(request,
                  "head/book.html",
                  {
                      'globals':Globals,
                      'date': datetime.date.today(),
                      "book": book,
                      'lends': lends,
                      'late_fees': late_fees,
                      'is_borrowed': is_borrowed,
                      'days_ago': days_ago,
                      "types":TYPES,
                  })


@login_required(login_url="/login")
def borrow(request):
    username = request.POST.get("username", None)
    bookID = request.POST.get("bookID", None)
    date = request.POST.get("date", None)
    if date is None:
        date = datetime.date.today()
    else:
        date_arr = [int(x) for x in date.split("-")]
        
    if username is None or bookID is None:
        return render(request,
                      "head/borrow.html", {
                          'globals': Globals,
                          "borrowed": 4,
                          "date_add": date.isoformat(),
                          'date': datetime.date.today()
                      })
    
    book = get_object_or_404(Book, accession_number=bookID)
    user = get_object_or_404(ModUser, username=username)

    lends = Lend.objects.filter(user=user,returned=False)
    if len(lends) > MAX_NUM_OF_BOOKS_TO_BORROW:
        borrowed = 3
    else:
        lends = Lend.objects.filter(book=book,user=user,returned=False)
        if len(lends) != 0:
            borrowed = 0
        elif len(lends) == 1 and lends.user == user:
            borrowed = 2
        else:
            ## the book can be lended
            lend_obj = Lend.objects.create(book=book,user=user, lending_date=date)
            date = [int(_) for _ in date.split("-")]
            lend_obj.date = datetime.date(date[0],date[1],date[2])
            lend_obj.save()
            book.state = 2
            book.save()
            borrowed = 1            
            
    ## borrowed has the following values:
    ## 0 - book is already borrowed by someone
    ## 1 - book was successfully borrowed
    ## 2 - book is already borrowed by the same user
    ## 3 - User has borrowed MAX_NUM_OF_BOOKS_TO_BORROW books already
    ## 4 - username and bookID were not given
    
    return render(request, 'head/borrow.html', {
        'globals': Globals,
        'date': datetime.date.today(),
        'date_val': date,
        'borrowed': borrowed,
        'book': book,
        'got_user': user,
        'book_acc': borrowed
    })




@login_required(login_url="/login")
def return_check_fees(request):
    bookID = request.GET.get("bookID", None)
    if request.method == "POST":
        bookID = request.POST.get("bookID", None)
        if bookID == None:
            return HttpResponseNotFound()
        else:
            book = get_object_or_404(Book, accession_number=bookID)
            lends = Lend.objects.filter(book=book) ## code to return book
            for _ in lends:
                _.set_returned()
                _.save()
            return render(request,
                          'head/return.html',
                          {
                              'globals': Globals,
                              'date': datetime.date.today(),
                              'code': "book_returned",
                              'lend_obj': lends[0]
                          }
            )
    if bookID is None:
        return render(request,
                      'head/return.html',
                      {
                          'globals': Globals,
                          'date': datetime.date.today(),
                          'code': 'None'
                      }
        )
    books = Book.objects.filter(accession_number=bookID,state=0)
    if len(books) != 1:
        return render(request,
                      'head/return.html',
                      {
                          'globals': Globals,
                          'date': datetime.date.today(),
                          'code':"not_found",
                          'accession_number': bookID
                      }
        )
    else:
        lend_obj = Lend.objects.filter(book__accession_number=bookID, returned=False)
        if len(lend_obj) == 1:
            lend_obj = lend_obj[0]
        late_fees = lend_obj.get_late_fees()
        return render(request,
                      'head/return.html',
                      {
                          'globals': Globals,
                          'date': datetime.date.today(),
                          'code':'success',
                          'lend_obj': lend_obj,
                          'late_fees': late_fees,
                          'has_late_fees': late_fees == 0
                      }
        )



@login_required(login_url="/login")
def return_book(request):
    pass
