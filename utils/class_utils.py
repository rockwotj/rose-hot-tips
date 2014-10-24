'''
Created on Oct 21, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb


def get_instructor_key_from_username(username):
    """ Example for Dave Fisher username: fisherds """
    return ndb.Key("Instructor", username)

def get_course_key_from_course_id(course_id):
    """ ex. for Intro to Software Dev. course_id: CSSE120 """
    return ndb.Key("Course", course_id)

def get_term_key_from_code(termcode):
    """ ex. for 2014 Fall Qtr. termcode: 201410 """
    return ndb.Key("Term", termcode)