# -*- coding: utf-8 -*-
from difflib import SequenceMatcher

from django.utils.encoding import smart_str

'''
def search(needle, heystack):
    needle = smart_str(needle.lower())
    heystack = smart_str(heystack.lower())
    if len(needle) == 0:
        return heystack
    needlel = needle.split(" ") ## get a list of all the words in the needle
    ranks = []
    heystackl = heystack.split(" ")
    if len(needlel) == 1:
        for each in heystackl:
            if needle in each:
                ranks.append(1./(len(heystack) - heystack.index(each)))
            else:
                seq = SequenceMatcher(None, needle, each)
                ranks.append(round(seq.ratio(), 3))
        return max(ranks) ## return the highest rank
    else:        
        for needeach in needlel:
            for heyeach in heystackl:
		ranks.append([])
                if needeach in enumerate(heyeach):
                    ranks[-1].append(
                            1 - 1./max(len(heystack) - heystack.index(heyeach),1))
                else:
                    seq = SequenceMatcher(None, needeach, heyeach)
                    ranks[-1].append(seq.ratio())
        rank_out = []
        for each in ranks:
            if each.__class__ == float:
                rank_out.append(each)
            else:
                rank_out.append(max(each))
        return sum(rank_out) / len(rank_out)

    return None
'''

def searchGenericField(searchstr, genericField):
    books = []
    genLinkQuerySet = genericField.value.all()

    for genLink in genLinkQuerySet:
        rank = search(searchstr, genLink.value)
        if rank > 0.6:
            books.append((genLink.book, rank))
    books = sorted(books, key=lambda book: book[1], reverse=True)
    books = [book[0] for book in books]
    return books


def searchBookAuthor(searchstr, bookQuerySet):
    searchstr = searchstr.strip(" ")
    books = []
    directSearch =  bookQuerySet.filter(author__name__contains = searchstr)
    perWordSearch = [ bookQuerySet.filter(author__name__contains = _) for _ in searchstr.split(" ")]
    if directSearch.count() > 0:
        return directSearch
    else:
        for _ in perWordSearch:
            if _.count() > 0:
                for book in _:
                    books.append(book)
        return books


def searchBookTitle(searchstr, bookQuerySet):
    searchstr = searchstr.strip(" ")
    books = []
    directSearch =  bookQuerySet.filter(title__contains = searchstr)
    perWordSearch = [ bookQuerySet.filter(title__contains = _) for _ in searchstr.split(" ")]
    if directSearch.count() > 0:
        return directSearch
    else:
        for _ in perWordSearch:
            if _.count() > 0:
                for book in _:
                    books.append(book)
        return books


def searchBookKeywords(searchstr, bookQuerySet):
    searchstr = searchstr.strip(" ")
    books = []
    directSearch =  bookQuerySet.filter(keywords__name__contains = searchstr)
    perWordSearch = [ bookQuerySet.filter(keywords__name__contains = _) for _ in searchstr.split(" ")]
    if directSearch.count() > 0:
        return directSearch
    else:
        for _ in perWordSearch:
            if _.count() > 0:
                for book in _:
                    books.append(book)
        return books
