'''
Created on Oct 21, 2014
@author: rockwotj
'''
import urllib2

from google.appengine.ext import ndb


def get_user_key_from_email(email):
    return ndb.Key("User", email.lower())

def get_user_key(user):
    return get_user_key_from_email(user.email())

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