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
    """ Deletes all sections and the termcode for a term. """
    section_keys = models.Section.query(models.Section.term == get_term_key(termcode), keys_only=True)
    ndb.delete_multi(section_keys)
    get_term_key(termcode).delete()

def get_course_reviews(course_id):
    """ Returns all the reviews for a course. """
    return get_course_reviews_from_key(get_course_key(course_id))

def get_course_reviews_from_key(course_key):
    """ Returns all the reviews for a course key. """
    return models.Review.query(models.Review.course == course_key).order(-models.Review.date_added)

def get_instructor_reviews(username):
    """ Returns all the reviews for a course. """
    return get_instructor_reviews_from_key(get_instructor_key(username))

def get_instructor_reviews_from_key(instructor_key):
    """ Returns all the reviews for a course key. """
    return models.Review.query(models.Review.instructor == instructor_key).order(-models.Review.date_added)