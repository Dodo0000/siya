# -*- coding: utf-8 -*-
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
'''


from head.models import BookSaver, Book, Lend, Publisher, Gifter
from account.models import ModUser
from settings.models import Globals, AccessionNumberCount, addGlobalContext
from settings.models import no_to_en
from settings.models import TYPES
from restructuredText.models import RestructuredText
from miscFields.models import GenericField

from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.text import slugify
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import datetime
import json
import time

from fuzz.search import searchBookTitle, searchBookAuthor, searchBookKeywords
from fuzz.search import searchGenericField

# Create your views here.


config = Globals()


TIME_PERIOD = config.config.getint('misc', 'report_time_period')  # months

LATE_FEES_PRICE = config.misc['late_fees_price']  # rupees per day
# number of days for which a book is to be borrowed
# max number of books member can borrow at once
NO_DAYS_TO_BORROW_BOOK = config.books['borrow_max_days']

MAX_NUM_OF_BOOKS_TO_BORROW = int(config.books['borrow_max_books'])

NO_OF_BOOKS_PER_PAGE = 10

NO_OF_ROWS_IN_ENTRY = 2

GLOBAL_CONTEXT = {
    "globals": config,
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
        '('][x]: str(x) for x in range(0, 10)
    }


def validateEmail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def toint(val, lang="EN"):
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


# #############################################################################
# ############################## AJAX CALL VIEWS ##############################


@login_required(login_url="/login/")
def does_the_accession_number_exist(request, accNo):
	books_no = Book.objects.filter(accession_number=accNo, state=0).count()
        return JsonResponse({'exists': books_no})


@login_required(login_url="/login/")
@permission_required(
        ("head.add_book", "head.change_book"), login_url="/login/")
def validate_book(request):
    '''
    checks if book with the given accession number exists
    returns True if it does,
    false if it doesn't.
    '''
    acc_no = request.GET.get('accNo', None)
    if acc_no is None:
        return JsonResponse({"data_correct": False, "valid": False})
    is_valid = -1
    if acc_no is not None:
        is_valid = int(
                len(Book.objects.filter(accession_number=acc_no, state=0)) > 0)

    json_dict = {
        'data_correct': True,
        "exists": is_valid,
        "accNo": acc_no
        }

    return JsonResponse(json_dict)


@login_required(login_url="/login/")
@permission_required(
        ("head.add_book", "head.change_book"),
        login_url="/login/")
def add_book(request):
    '''
    the add_book function takes too long, and since this function is executed
    many times, sometimes at once by multiple users, it needs to be resized
    into something managable, I don't know how though :(
    '''
    t0 = time.time()
    config.reload()

    # all_attrs is a list of all the default fields for HADES - such as
    # title, authors etc. More in config.ini
    all_attrs = [_[1] for _ in config.config['columns'].items()]

    each = dict()   # store post data
    STATE = 0

    books_list = []  # this is a list of all the books added, which will be
    # saved at once using bulk_save

    for _ in all_attrs:
        # check which of the all_attrs are sent by javascript
        each[_] = request.POST.get(_)

    if "," in str(each['acc_no']):
        # if the accession numbers are seperated by a ',' then add the same
        # info should be aded for each of the accession numbers specified
        acc_list = [_.strip(" ") for _ in each['acc_no'].split(",")]

    elif "-" in str(each['acc_no']):
        # if the accession numbers are seperated by a '-', then a range is
        # specified and the same info is added to the range a - b
        acc_strip = [int(_) for _ in each['acc_no'].split("-")]
        if len(acc_strip) != 2:
            raise TypeError("Range Too Many or To Few (not 2) ")
        acc_list = list(range(acc_strip[0], acc_strip[1]+1))
    else:
        # if only a single accession number is given, add only that to acc_list
        acc_list = [each['acc_no']]

    for val in acc_list:
        # check if the accession number is a string, if it is a string, then
        # stip off all the space, else if it is an integer, then let it be
        if val.__class__ == str:
            accession_number = val.strip(" ")
        else:
            accession_number = val

        # the three fields that are necessary for each book are:
        #           1) Accession Number
        #           2) No. of pages
        #           3) Title
        # if any of these fields is not given, then the STATE is changed to -1
        # and the book is not saved.
        if accession_number in [None, "None", 0, "0", ""] or "-" in accession_number:
            STATE = -1
            continue
        if each['no_of_pages'] in [None, "", 0, "0"] or '-' in each['no_of_pages']:
            STATE = -1
            continue
        if each['title'] in [None, "", 0, "0"]:
            STATE = -1
            continue

        # either create a new book or edit an already existing book
        book_was_created = True
        try:
            book = Book.objects.filter(
                    accession_number=toint(accession_number))
            if book.count() == 0:
                raise ObjectDoesNotExist()
            else:
                book = book[0]
            book_was_created = False
        except ObjectDoesNotExist:
            book = Book.objects.create(
                    accession_number=toint(accession_number),
                    title=each['title'].lower(),
                    no_of_pages=toint(
                        each['no_of_pages']))

        # if the book was found, the title, page No. and accession number
        # can also to change
        if book_was_created is False:
            book.title = each['title'].lower()
            book.no_of_pages = toint(each['no_of_pages'])

        authors = each['auth'].lower().split(",")

    book.author.clear()
    for author_name in each['auth'].lower().split(","):
        # when saving, author names are seperated by a ,
        author_name = author_name.strip(" ")
        author = book.author.get_or_create(
            name=author_name,
            slug=slugify(author_name))
        if (
                each['pub_place'] is None or
                each['pub_year'] is None or
                each['pub_name'] is None
        ) is False:
            publisher = Publisher.objects.get_or_create(
                place=each['pub_place'].lower(),
                name=each['pub_name'].lower(),
                year=toint(each['pub_year']))
            if publisher[1]:
                publisher = publisher[0]
                publisher.save()
            else:
                publisher = publisher[0]
            book.publisher = publisher
        book.call_number = each['call_no']

        # it takes 1.28746032715e-05 seconds for code from here **
        if (each['ser'] is None) is False:
            book.series = each['ser'].lower()

        if (each['edtn'] is None) is False:
            book.edition = each['edtn'].lower()

        if (each['isbn'] is None) is False:
            book.isbn = each['isbn']

        if (each['price'] is None) is False:
            book.price = each['price']
        # to here **

        # this if statement takes 0.153175115585 seconds if the nested if
        # returns true
        if each['gftd_name'] is not None:
            gifter_name = each['gftd_name'].lower()
            gifter_phn = each['gftd_phn']
            gifter_email = each['gftd_email']
            # only create new database object if the data has been changed
            if book.gifted_by is None or (gifter_name not in [None, ''] or gifter_name.lower() != book.gifted_by.get_name().lower() or gifter_email != book.gifted_by.get_email() or gifter_phn != book.gifted_by.get_phone_no()):
                gifter = Gifter.objects.get_or_create(gifter_name=gifter_name)
                gifter = gifter[0]
                if gifter_phn.isdigit():
                    gifter.phone = gifter_phn
                if validateEmail(gifter_email):
                    gifter.email = gifter_email
                gifter.save()
                book.gifted_by = gifter

        if each['vol'] is not None and each['vol'] != "None":
            if each['vol'].isdigit() is True:
                book.volume = int(each['vol'])
            else:
                book.volume = acc_list.index(val) + 1
        else:
            book.volume = acc_list.index(val) + 1

        keywords = each['kwds'].split(",")
    book.keywords.clear()
    for keyword in keywords:
        keyword = keyword.strip(' ')
        book.keywords.get_or_create(
            name=keyword,
        slug=slugify(keyword))

        # this stores the name of the person who uodated the book, along with
        # the date and time of modification
        bookSaver = BookSaver.objects.create(user=request.user)
        book.saved_by.add(bookSaver)
        books_list.append(book)
        # generic fields
        for field in GenericField.objects.all():
            program_key = field.get_programatic_key()
            key = '__gen_' + program_key
            if request.POST.get(key) is not None:
                link = field.value.get_or_create(book=book)
                link = link[0]
                link.value = request.POST.get(key)
                link.save()

        STATE = 0  # STATE = 0 menas teh book was saved

    t1 = time.time()
    print t1 - t0

    for book in books_list:
        book.state = 0
        book.save()

    if STATE == 0:
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})

##############################################################################


@login_required(login_url="/login")
@permission_required(("head.add_book", "head.change_book"), login_url="/login/")
def editEntry(request, id):
    config.reload()
    book_exists = True
    if id is not None:
        books = Book.objects.filter(id=id)
        if len(books) < 1:
            return HttpResponseRedirect(reverse("entry"))
        else:
            book = books[0]
        clear_fields = False
    else:
        book_exists = False
        book = None
        clear_fields = True

    columns_for_table = list(enumerate(config.books_columns.items(), 1))

    columns_for_generic_fields = list(enumerate([(x.key, "__gen_"+x.get_programatic_key()) for x in GenericField.objects.all()]))

    for _ in columns_for_generic_fields:
        columns_for_table.append(_)

    columns_for_entry = list(enumerate((_[1] for _ in columns_for_table), 1))

    columns_for_entry_div = [columns_for_entry[c:c+NO_OF_ROWS_IN_ENTRY] for c in range(0, len(columns_for_entry)+1, NO_OF_ROWS_IN_ENTRY)]
    columns_for_generic_fields_div = [columns_for_generic_fields[c:c+NO_OF_ROWS_IN_ENTRY] for c in range(0, len(columns_for_generic_fields)+1, NO_OF_ROWS_IN_ENTRY)]

    total_no_of_cols_table = len(columns_for_table)
    total_no_of_cols_entry = len(columns_for_entry)

    if total_no_of_cols_entry <= 12:
        div_len = 12 / total_no_of_cols_entry
        div_offset = (12 - (div_len * total_no_of_cols_entry)) / 2
    else:
        div_len = total_no_of_cols_entry / 12
        div_offset = ((div_len * total_no_of_cols_entry) - 12) / 2


    return render(request,
                  "head/entry.html", addGlobalContext({
                      'globals': config,
                      'date': datetime.date.today(),
                      "columns_for_table": columns_for_table,
                      "columns_for_entry": columns_for_entry,
                      "columns_for_entry_div": columns_for_entry_div,
                      'no_of_rows': NO_OF_ROWS_IN_ENTRY,
                      'div_len': div_len,
                      'book': book,
                      'is_edit': int(book_exists),
                      'div_offset': div_offset,
                      'total_columns_table': total_no_of_cols_table,
                      'total_columns_entry': total_no_of_cols_entry,
                      'columns_entry_json': json.dumps(columns_for_entry, indent=4),
                      'columns_table_json': json.dumps(columns_for_table, indent=4),
                      'largest_accession_number': AccessionNumberCount.get_no(),
                      'clear_fields': int(clear_fields)
                  }))


@login_required(login_url="/login/")
@permission_required(("head.change_book", "head.add_book"), login_url="/login/")
def entry(request):
    return editEntry(request, None)


@login_required(login_url="/login")
def report(request):
    config.reload()
    no_of_months = TIME_PERIOD
    this_date = datetime.date.today()
    start_month = this_date.month - no_of_months
    if start_month < 0:
        start_date = datetime.date(this_date.year - 1, 12 - start_month, this_date.day)
    else:
        start_date = datetime.date(this_date.year, start_month, this_date.day)
    time_period = this_date - start_date

    books_cataloged_in_tp = Book.objects.exclude(
        accessioned_date__gte=this_date, state=0).filter(
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
                  {'globals': config,
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
    config.reload()
    home_template = "head/home.html"
    context = addGlobalContext({"popular_books": Book.objects.order_by("?")[0:3]})
    return render(request, home_template, context)


def about(request):
    config.reload()
    about_template = "head/about.html"
    return render(request, about_template, addGlobalContext({"body_code": RestructuredText.objects.get(name="homeBody").get_html()}))


@login_required(login_url="/login")
def dashboard(request):
    import calendar
    config.reload()

    logged_in = request.META.get('logged_in', None)
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=TIME_PERIOD*30)

    # problem, the _gte filter with `today' excludes the data entered on today...fix this
    time_period = today - start_date
    members_added_during_tp = ModUser.objects.exclude(
            date_joined__gte=today).filter(date_joined__gte=start_date)
    total_members = ModUser.objects.all()
    books_cataloged_during_tp = Book.objects.exclude(
            accessioned_date__gte=today).filter(accessioned_date__gte=start_date, state=0)
    recently_added_books = list(Book.objects.filter(state=0, accessioned_date=datetime.date.today()).order_by("-accessioned_date"))[:20]
    recently_added_books.reverse()
    total_books = Book.objects.all()

    return render(request, "head/dashboard.html", addGlobalContext({
        "members_added_during_tp": members_added_during_tp,
        "members_added_before_tp": total_members.exclude(date_joined__gte=start_date),
        'total_members': total_members,
        'books_cataloged_during_tp': books_cataloged_during_tp,
        'books_cataloged_before_tp': total_books.exclude(accessioned_date__gte=start_date),
        'total_books': total_books,
        'time_period': time_period.days / 30,
        'start_date': start_date,
        'recently_added_books': recently_added_books,
        'recently_added_members': ModUser.objects.order_by("-date_joined"),
        'logged_in': logged_in
    }))


@login_required(login_url="/login")
@permission_required("head.delete_book")
def deleteBookConfirm(request, id):
    config.reload()
    if id.isdigit():
        book = Book.objects.filter(id=id, state=0)
        len_book = book.count()
        if len_book == 0 or len_book > 1:
            context_dict = {
                    "state": -1,
                    "message": "The No. of  book With ID `{}` Was not 1".format(id),
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
    return render(request, "head/delete_book.html", addGlobalContext(context_dict))


@login_required(login_url="/login")
@permission_required("head.delete_book")
def deleteBook(request, id):
    config.reload()
    book = Book.objects.get(id=id)
    book.discard()
    context_dict = {"book": book}
    context_dict.update(GLOBAL_CONTEXT)
    return render(request, "head/deleted_book.html", addGlobalContext(context_dict))


def searchBook(request):
    config.load()
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
    < Note : In Step 2c, meaning of the word "most" is very flexible. >
    '''
    page = request.GET.get("page", 1)
    all_books = Book.objects.filter(state=0)    # state - 0 is books which are available

    if value is not None:
        value = value.split(" ")
        if type_.startswith("."):  # search in generic fields. ( generic field types start with .)
            gen_field = GenericField.objects.filter(key=type_[1:])
            if len(gen_field) == 1:
                gen_field = gen_field[0]
                books = searchGenericField(" ".join(value), gen_field)
        if type_ == config.text['title']:
            books = searchBookTitle(" ".join(value), all_books)
        elif type_ == config.text['call_number']:
            books = Book.objects.filter(call_number__contains=value[0], state=0)
        elif type_ == config.text['accession_number']:
            books = Book.objects.filter(Q(accession_number=no_to_en(value[0])),
                Q(state=0))

        elif type_ == config.text['keyword']:
            books = searchBookKeywords(" ".join(value), all_books)
        elif type_ == config.text['publisher']:
            books = Book.objects.filter(publisher__name__contains=value[0], state=0)
            for each in value[1:]:
                bookf = books.filter(publisher__name__contains=each, state=0)
                if bookf.count() > 0:
                    books = bookf
                else:
                    break
        elif type_ == config.text['author']:
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
    total_book_len = len(booklist)
    try:
        booklist = paginator.page(page)
    except PageNotAnInteger:
        booklist = paginator.page(1)
    except EmptyPage:
        booklist = paginator.page(paginator.num_pages)
    return render(request,
                  "head/search_books.html",
                  addGlobalContext({
                      'total_books_len': total_book_len,
                      "books": booklist,
                      "book_pages": list(range(1, min(paginator.num_pages+1, 9))),
                      "value": " ".join(value),
                      "type": type_,
                      "not_found": not_found
                  }))


def bookInfo(request, id):
    config.reload()
    books = Book.objects.filter(id=id)
    if books.count() == 0:
        return HttpResponse("Book Not Found")
    else:
        book = books[0]

    lends = Lend.objects.filter(book=book)

    if lends.count() > 0:
        lends = lends[len(lends)-1]
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

    if lends is not None:
        late_fees = lends.get_late_fees()
    else:
        late_fees = 0

    # get data for all generic fields.
    # if the book doesnt have value for generic field, give an empty string :)
    generic_fields = []

    for _ in GenericField.objects.all():
        try:
            genFieldLink = _.value.get(book=book)
        except ObjectDoesNotExist:
            genFieldLink = None
        if genFieldLink is not None:
            generic_fields.append((_, genFieldLink.get_value()))
        else:
            generic_fields.append((_, ""))

    '''
    when someone searches for the book, ?source=search is appended to the url.
    WHen sources=search is found in request.GET, a view is added to the book,
    then the user is redirected to a url for the book without the
    ?source=search tail. This is because views are only added when a book is
    searched, not simply when the page is refreshed.
    '''

    '''
    If the book is simply refreshed, then views are not added, but if the book
    is searhced for, or found some other way,
    then a view is added
    '''
    get_source = request.GET.get("source", None)
    refreshedHttpRedir = HttpResponseRedirect(
            reverse(
                'book',
                kwargs={'id': book.id}) + "?search=refreshed")
    if get_source != "refreshed" and get_source is not None:
        book.add_view()
        return refreshedHttpRedir
    elif get_source == "":
        # don't add view if nothing is specified
        return refreshedHttpRedir

    return render(request,
                  "head/book.html",
                  addGlobalContext({
                      "book": book,
                      'lends': lends,
                      'late_fees': late_fees,
                      'is_borrowed': is_borrowed,
                      'days_ago': days_ago,
                      "types": TYPES,
                      "genericFields": generic_fields
                  }))


@login_required(login_url="/login")
@permission_required(("head.change_lend", "head.add_lend"))
def __borrow__(request, acc_no=None, username=None):
    config.reload()
    username = request.POST.get("username", None)
    bookID = request.POST.get("bookID", None)
    date = request.POST.get("date", None)
    if date is None:
        date = datetime.date.today()
    else:
        date_arr = [int(x) for x in date.split("-")]

    if username is None or bookID is None:
        return render(request,
                      "head/borrow.html", addGlobalContext({
                          "borrowed": 4,
                          "date_add": date.isoformat(),
                      }))

    book = get_object_or_404(Book, accession_number=bookID)
    user = get_object_or_404(ModUser, username=username)

    lends = Lend.objects.filter(user=user, returned=False)
    if lends.count() > MAX_NUM_OF_BOOKS_TO_BORROW:
        borrowed = 3
    else:
        lends = Lend.objects.filter(book=book, user=user, returned=False)
        if lends.count() != 0:
            borrowed = 0
        elif lends.count() == 1 and lends.user == user:
            borrowed = 2
        else:
            # the book can be lended
            lend_obj = Lend.objects.create(book=book, user=user, lending_date=date)
            date = [int(_) for _ in date.split("-")]
            lend_obj.date = datetime.date(date[0], date[1], date[2])
            lend_obj.save()
            book.state = 2
            book.save()
            borrowed = 1

    # borrowed has the following values:
    # 0 - book is already borrowed by someone
    # 1 - book was successfully borrowed
    # 2 - book is already borrowed by the same user
    # 3 - User has borrowed MAX_NUM_OF_BOOKS_TO_BORROW books already
    # 4 - username and bookID were not given

    context = addGlobalContext({
        'date_val': date,
        'borrowed': borrowed,
        'book': book,
        'got_user': user,
        'book_acc': borrowed
    })
    if username is not None:
        context.update({'username': username})
    if acc_no is not None:
        context.update({"acc_no": acc_no})

    return render(request, 'head/borrow.html', context)


@login_required(login_url="/login")
@permission_required(("head.change_lend", "head.add_lend"))
def borrow(request):
    return __borrow__(request)


@login_required(login_url="/login")
@permission_required(("head.change_lend", "head.add_lend"))
def borrow_with_acc_no(request, acc_no):
    return __borrow__(acc_no=acc_no)


@login_required(login_url="/login")
@permission_required(("head.change_lend", "head.add_lend"))
def borrow_with_username(request, username):
    return __borrow__(username=username)


@login_required(login_url="/login")
@permission_required("head.change_lend")
def return_check_fees(request):
    config.reload()
    bookID = request.GET.get("bookID", None)
    if request.method == "POST":
        bookID = request.POST.get("bookID", None)
        if bookID is None:
            return HttpResponseNotFound()
        else:
            book = get_object_or_404(Book, accession_number=bookID)
            lends = Lend.objects.filter(book=book)  # code to return book
            for _ in lends:
                _.set_returned()
                _.save()
            return render(request,
                          'head/return.html',
                          addGlobalContext({
                              'code': "book_returned",
                              'lend_obj': lends[0]
                          })
                          )
    if bookID is None:
        return render(request,
                      'head/return.html',
                      addGlobalContext({
                          'code': 'None'
                      })
                      )
    books = Book.objects.filter(accession_number=bookID)
    if books.count() != 1:
        return render(request,
                      'head/return.html',
                      addGlobalContext({
                          'code': "not_found",
                          'accession_number': bookID
                      })
                      )
    else:
        lend_obj = Lend.objects.filter(book__accession_number=bookID, returned=False)
        if lend_obj.count() == 1:
            lend_obj = lend_obj[0]
        late_fees = lend_obj.get_late_fees()
        return render(request,
                      'head/return.html',
                      addGlobalContext({
                          'code': 'success',
                          'lend_obj': lend_obj,
                          'late_fees': late_fees,
                          'has_late_fees': late_fees == 0
                      })
                      )


@login_required(login_url="/login")
def return_book(request):
    pass


def copyBook(request):
    return render(request, "head/copyBook.html", addGlobalContext())


@login_required(login_url="/login")
def reviveBook(request, id):
    books = Book.objects.filter(id=id)
    if books.count() == 1:
        books[0].bring_back()
    else:
        print "there are many books with accession number " + str(accNo)
    return bookInfo(request, id=id)
