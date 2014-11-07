'''
Created on Oct 21, 2014
@author: rockwotj
'''
import urllib2

from google.appengine.ext import ndb
from models import User
import logging

def get_user_key_from_email(email):
    return ndb.Key("User", email.lower())

def get_user_key(user):
    return get_user_key_from_email(user.email())

def is_validated(user):
    user_entity = get_user_key(user).get()
    if user_entity:
        return user_entity.verified
    else:
        return False

def set_validate(user, valid):
    user_key = get_user_key(user)
    user_entity = user_key.get()
    if user_entity:
        user_entity.verified = valid
    else:
        user_entity = User(key=user_key, verified=valid)
        user_entity.put()

def validate_user(username, password):
    """ Checks that a user can login to the schedule lookup page to validate that they have correct KERBEROS identification. """
    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # the url to check with
    url = "https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl"
    # add the password for the URL
    password_mgr.add_password(None, url, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    # create private class variable "__opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)
    try:
        opener.open(url)
        return True
    except:
        return False
