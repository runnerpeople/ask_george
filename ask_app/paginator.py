#!usr/bin/python
# -*- coding: utf-8 -*-
import collections,math
__author__ = "runnerpeople"

class PageNotAnInteger(Exception):
    pass

class EmptyPage(Exception):
    pass


class Paginator(object):
    def __init__(self,object_list,pages):
        self.object_list = object_list
        self.pages = pages
        self.num_pages = int(math.ceil(len(self.object_list)/float(self.pages)))

    def validate(self,number_page):
        try:
            number_page = int(number_page)
        except (TypeError,ValueError):
            raise PageNotAnInteger("That's page_number not a integer")
        if number_page<1:
            raise EmptyPage("That's page_number less than 1")
        else:
            if number_page > self.num_pages:
                return self.num_pages
            else:
                return number_page



    def page(self,number_page):

        # For None and Not-Integer Type #
        try:
            number_page = int(number_page)
            if number_page==0:
                raise Exception
        except:
            number_page = 1

        number_page = self.validate(number_page)
        return Page(self.object_list[(number_page-1)*self.pages:(number_page)*self.pages], number_page, self)
        #except:
        #    return Page(self.object_list[(self.num_pages - 1) * self.pages:self.num_pages * self.pages], self.num_pages, self)



class Page(collections.Sequence):
    def  __init__(self,object_list,page_number,paginator):
        self.object_list = object_list
        self.page_number = page_number
        self.paginator = paginator

    def has_next(self):
        return self.page_number < self.paginator.num_pages

    def has_previous(self):
        return self.page_number > 1

    def previous_page_number(self):
        return self.paginator.validate(self.page_number-1)

    def next_page_number(self):
        return self.paginator.validate(self.page_number+1)


    #def previous_page(self,pages = 5):
    #    i = self.page_number
    #    paginate = []
    #    for count in range(pages):
    #        try:
    #            number = self.paginator.validate(i-count)
    #            paginator.append(0)
    #
    #        except:



    #def next_page(self):
    #    return self.paginator.page(self.page_number + 1)

    def __str__(self):
        return "Page %d of %d" % (self.page_number,self.paginator.num_pages)

    def __repr__(self):
        return "Page %d of %d" % (self.page_number, self.paginator.num_pages)

    def __getitem__(self, item):
        return list(self.object_list[item])

    def __len__(self):
        return len(self.object_list)



