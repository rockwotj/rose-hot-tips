'''
Created on Oct 21, 2014
@author: rockwotj
'''
from google.appengine.ext import ndb


def get_user_key_from_email(email):
    return ndb.Key("Entity", email.lower())

def get_user_key(user):
    return get_user_key_from_email(user.email)
