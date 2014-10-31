'''
Created on Oct 21, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb

import models


def get_instructor_key(username):
    """ Example for Dave Fisher username: fisherds """
    return ndb.Key("Instructor", username)

def get_course_key(course_id):
    """ ex. for Intro to Software Dev. course_id: CSSE120 """
    return ndb.Key("Course", course_id)

def get_term_key(termcode):
    """ ex. for 2014 Fall Qtr. termcode: 201410 """
    return ndb.Key("Term", termcode)

def get_section_key(course_section, termcode):
    """ ex. for 2014 Fall CSSE 120-01. course_section: CSSE120-01, termcode: 201410"""
    # The key's id will read CSSE120-01-201410
    # We do this so that we can over write sections if we reparse the data.
    return ndb.Key("Section", course_section + "-" + termcode)

def get_all_sections(termcode):
    """ Returns all the Section entities for a given term. termcode: 201410 """
    return models.Section.query(models.Section.term == get_term_key(termcode))

def get_all_termcodes():
    """ Returns all termcodes in order from most recent to oldest. """
    return models.Term.query().order(-models.Term.date_added)

def search_for_sections(query_string, termcode):
    """ TODO: """
    return None

def delete_termcode(termcode):
    """ TODO: Delete all sections, reviews and the termcode for a term. """
    section_keys = models.Section.query(models.Section.term == get_term_key(termcode), keys_only=True)
    ndb.delete_multi(section_keys)
