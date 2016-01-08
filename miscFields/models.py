# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_str

from head.models import Book
# Create your models here.

class GenericFieldLink(models.Model):
    '''
    this model stores the value in GenericField for each book
    '''
    value = models.TextField(null=True)
    book = models.ForeignKey(Book)

    def get_value(self):
        return smart_str(self.value)

    def get_book(self):
        return self.book

    def get_book_id(self):
        return self.book.id

    def __str__(self):
        return "value  for %s book" % self.book.get_title()


class GenericField(models.Model):
    '''
    this is a generic field for a book
    this can be anything you want it to be

    this has two attrs : 
    key - name of the field
    value - value that is stored for each book in the db
    '''
    key = models.CharField(max_length=255, default="What is My name?")
    value =  models.ManyToManyField(GenericFieldLink)

    def __str__(self):
        return self.key

    def get_key(self):
        '''return the key'''
        return smart_str(self.key)

    def get_value_obj(self, book_id):
        '''return the GenericFieldBookLink object for that book'''
        book = Book.objects.get(id=book_id)
        return value.get(book=book)

    def get_value(self, book_id):
        '''
        returns the value as unicode string
        '''
        return self.get_value_obj(book_id=book_id).get_value()

    def set_value(self, value, book):
        x = GenericFieldLink.objects.create(book=book,value=value)
        self.value.add(x)


    def get_programatic_key(self):
        '''
        return the key as something without spaces or other invalid chars
        '''
        return self.get_key().replace(" ", "_")

