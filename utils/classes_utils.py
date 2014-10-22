'''
Created on Oct 21, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb


def get_instructor_key_from_username(username):
    return ndb.Key("Instructor", username)

def get_course_key_from_course_id(course_id):\
    return ndb.Key("Course", course_id)

