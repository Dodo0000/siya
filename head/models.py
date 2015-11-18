'''
  ____             _   _       ___       ____            _ 
 |  _ \  ___  __ _| |_| |__   |_ _|___  |  _ \ ___  __ _| |
 | | | |/ _ \/ _` | __| '_ \   | |/ __| | |_) / _ \/ _` | |
 | |_| |  __/ (_| | |_| | | |  | |\__ \ |  _ <  __/ (_| | |
 |____/ \___|\__,_|\__|_| |_| |___|___/ |_| \_\___|\__,_|_|
                                                           
If you can keep your head when all about you   
    Are losing theirs and blaming it on you,   
If you can trust yourself when all men doubt you,
    But make allowance for their doubting too;   
If you can wait and not be tired by waiting,
    Or being lied about, don't deal in lies,
Or being hated, don't give way to hating,
    And yet don't look too good, nor talk too wise: 

'''
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
# Create your models here
from account.models import ModUser
from settings.models import Globals

import datetime


def make_title(title):
    title = title.strip(" ")
    return title[0].upper() + title[1:]
        

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


def cint(v, b, lang="EN"):
    '''
    b = To Convert or not
    v = value to convert
    '''
    if b == 0 or b == False:
        return v
    else:
        return toint(v, lang)


class Publisher(models.Model):
    '''
    Model that holds the attributes of a publisher
    '''
    name = models.CharField(max_length=255, db_index=True)
    place = models.CharField(max_length=255, db_index=True)
    year = models.CharField(max_length=10, db_index=True)

    def get_name(self):
        return smart_str(self.name)

    def get_place(self):
        return smart_str(self.place)
    def get_year(self):
        return smart_str(self.year)
    
    def __str__(self):
        if self.year == u"0" and self.place != None and self.name != None:
            return smart_str(u"{0}, {1}".format(
                self.name,
                self.place))
        elif self.place == None and self.year != None and self.name != None:
            return smart_str(u"{0} in {1}".format(
                self.name,
                self.year))
        else:
            return smart_str(u"{0}, {1} in {2}".format(
                self.name,
                self.place,
                self.year))

    def __catalog__(self):
        if self.year == u"0" and self.place != None and self.name != None:
            return smart_str(u"{1}: {0}".format(
                self.name,
                self.place))
        elif self.place == None and self.year != None and self.name != None:
            return smart_str(u"{0}: {1}".format(
                self.name,
                self.year))
        else:
            return smart_str(u"{1}: {0}: {2}".format(
                self.name,
                self.place,
                self.year))





class Author(models.Model):
    '''
    Model for Author Class
    Describes the properties of an author
    '''
    name = models.CharField(max_length=100)
    slug = models.SlugField(db_index=True)

    def get_name(self):
        '''
        the data entered for an anuthor is in the format:
        last_name, first_name
        '''
        name_list = self.name.split(",")
        name_list.reverse()
        return " ".join(name_list)

    def get_catalog_name(self):
        name_list = self.name.split(",")
        if name_list.__len__() >= 2:
            return self.name
        elif len(name_list) == 1:
            return ",".join(name_list[0].split(" "))
            
    def __str__(self):
        return smart_str(self.name)
    
class KeyWord(models.Model):
    '''
    The Keyword Model for Book class.
    It has a ManyToMany relationship with Book.
    synonymn to tags.
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True)

    def __str__(self):
        return smart_str(self.name.title())


class Lend(models.Model):
    user = models.ForeignKey(ModUser, db_index=True)
    book = models.ForeignKey('Book', db_index=True)
    lending_date = models.DateField(db_index=True)
    returned_date = models.DateField(null=True, db_index=True)
    returned = models.BooleanField(default=False, db_index=True)
    borrowed = models.BooleanField(default=False, db_index=True)


    def get_borrowed_time(self):
        dt = datetime.date.today() - self.lending_date
        return int(dt.days)
    
    def get_late_fees(self):
        borrowed_time = self.get_borrowed_time()
        max_days = Globals.books['borrow']['max_days']
        money_per_day = Globals.late_fees_rate
        if borrowed_time > max_days:
            return money_per_day *  (borrowed_time - max_days)
        else:
            return 0

    def set_returned(self,date=datetime.datetime.today()):
         self.returned_date = date
         self.returned= True
         self.save()
         self.book.state = 0
         self.book.save()

    def __str__(self):
        return "{0}, {1}".format(
                str(self.book),
                self.lending_date.strftime("%A %eth %B, %Y")
                )


class Gifter(models.Model):
    '''
    This class describes the person who gifted this book
    '''
    date_given = models.DateField(auto_now_add=True, db_index=True)
    gifter_name = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    phone = models.IntegerField(null=True)

    def get_email(self):
        return self.email

    def get_phone_no(self):
        return self.phone

    def get_name(self):
        return smart_str(self.gifter_name)

    def __str__(self):
        if self.email is None:
            if self.phone is None:
                return "{} on {}".format(self.gifter_name,self.date_given)
            else:
                return "{0}, phone no.: {1} on {2}".format(self.gifter_name,self.phone,self.date_given)
        elif self.phone is None:
            if self.email is None:
                return "{0} on {1}".format(self.gifter_name,self.date_given)

            else:
                return "{0}, email: {1} on {2}".format(self.gifter_name,self.email,self.date_given)
        else:
            return "{0}, phone: {1}, email: {2} on {3}".format(self.gifter_name,self.phone,self.email,self.date_given)
    


class Book(models.Model):
    '''
    accession number increases by +1 for each new entry; kinda like the
    primary number. Each book as a unique accession number
    '''
    accession_number = models.CharField(max_length=9, db_index=True)
    accessioned_date = models.DateField(auto_now=True, db_index=True)
    '''
    call number describes the type of book, such as - is it a story book?
    Is it a nepali book? english book? Hindi book? Is it fiction? reference?
    etc
    '''
    call_number = models.CharField(max_length=20, null=True,blank=True, db_index=True)
    author = models.ManyToManyField(Author,db_index=True)  # author of the book
    title = models.CharField(max_length=255,db_index=True)    # name of the book
    no_of_pages = models.IntegerField(db_index=True)
    '''
    If the book is part of a series,
    this tells the number in which the book falls into the series
    '''

    language = models.CharField(max_length=5,default="EN",db_index=True)
    publisher = models.ForeignKey(Publisher,null=True,blank=True,db_index=True)
    series = models.CharField(max_length=20,blank=True,null=True,db_index=True)
    edition = models.CharField(max_length=100,blank=True,null=True,db_index=True)
    price = models.CharField(max_length=255,null=True,blank=True,db_index=True)
    volume = models.CharField(max_length=10,null=True,blank=True,db_index=True)
    keywords = models.ManyToManyField(KeyWord,db_index=True)

    
    isbn = models.CharField(max_length=13,null=True,db_index=True)
    '''
    State has three values: 
    0 - Is available
    1 - Is Discarded
    2 - Is borrowed
    defaults to {0}
    '''
    state = models.IntegerField(default=0,db_index=True)
    '''
    The keywords describe in a more specific manner, the "personality" of the
    book which the call number failed to explain
    '''
    gifted_by = models.ForeignKey(Gifter,null=True,db_index=True)



    def bring_back(self):
        self.state = 0
        self.save()

    def discard(self):
        self.state = 1
        self.save()

    def is_discarded(self):
        return self.state == 1


    @staticmethod
    def get_attr_list():
        return (
            'accNo',
            'callNo',
            'title',
            'author',
            'publisher',
            'no_of_pages',
            'keywords',
            'date_added'
        )
    
    def get_all_attr(self):
        return (
            ('Accession Number', self.accession_number),
            ('Call Number', smart_str(self.call_number)),            
            ('Title', smart_str(self.title)),
            ('Author', self.get_authors()),
            ('Publisher', self.get_publishers()),
            ('No. of Pages', self.no_of_pages),
            ('keywords', smart_str(self.get_keywords())),
            ('Date Added', self.accessioned_date),
            ("Series", self.get_series()),
            ("Edition", self.get_edition()),
            ("Price", self.get_price()),
            ("Volume", self.get_volume()),
            ("Gifted By", self.get_gifted_by()),
        )

    
    def get_accession_number(self):
        return smart_str(self.accession_number)

    def get_call_number(self):
        if self.language == "EN":
            return smart_str(self.call_number)
        else:
            call_no = "".join([str(cint(_,_ in NP_NUM.keys(), lang=self.language)) for _ in self.call_number])
            return smart_str(call_no)

    def get_language(self):
        return smart_str(self.language)

    def get_series(self):
        if self.series == None:
            return "No series"
        else:
            return smart_str(self.series)

    def get_edition(self):
        if self.edition == None:
            return "No edition"
        else:
            return smart_str(self.edition)

    def get_price(self):
        if self.price == None:
            return "No price"
        else:
            return smart_str(self.price)

    def get_volume(self):
        if self.volume is None:
            return 1
        else:
            return smart_str(self.volume)

    def get_gifted_by(self):
        if self.gifted_by == None:
            return "Not Gifted By Anyone"
        else:
            return smart_str(self.gifted_by.__str__())

    def get_title(self):
        return self.title

    def __str__(self):
        if self.title is not None:
            return smart_str(self.get_title())
        else:
            return ""

    '''
    What's up with all the get_* functions you ask?
    These functions help the template system display data in a meaningful way 
    is all.
    I don't see any other use for these.
    '''
    
    @staticmethod
    def get_largest_accession_number():
        return Book.objects.all().order_by("-accession_number")[0].accession_number

    def get_borrower(self):
        lends = Lend.objects.filter(book=self,returned=False)
        if len(lends) == 1:
            return lends[0].user
        else:
            return None

    def is_borrowed(self):
        return self.state == 2 

    def get_authors(self):
        author_list =  self.author.all()
        if len(author_list) > 0:
            return ",".join([smart_str(x.get_name()) for x in author_list])
        else:
            return "No Authors"

    def get_publishers(self):
        if self.publisher is not None:
            return self.publisher.__str__()
        else:
            return "No Publishers"
    

    def get_catalog_publishers(self):
        if self.publisher is not None:
            return self.publisher.__catalog__()
        else:
            return ""

    def get_keywords(self):
        if self.keywords is not None:
            return ", ".join([smart_str(
                each.__str__()) for each in self.keywords.all() if each.__str__() is not None])
        else:
            return "No Keywords"

    def set_borrowed_by(self, user, date=None):
        if user.is_authenticated():
            if len([1 for x in user.groups.values() if x['name'] == 'member']) != 0:
                lend_obj = Lend.objects.create(book=self, user = user)
                if date is not None:
                    try:
                        date = [int(_) for _ in x.split('-')]
                        lend_obj.date = datetime.date(
                            date[0].split(" "),
                            date[1].split(" "),
                            date[2].split(" "))
                    except:
                        raise TypeError(
                            "value of date `{}`: does not convert into year-month-day format".format(date))
                lend_obj.save()
                self.state = 2   #is borrowed 
                self.save()  #save book
            else:
                return 1
        else:
            return 1
        return 0
