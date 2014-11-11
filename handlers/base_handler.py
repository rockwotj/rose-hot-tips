'''
Created on Oct 16, 2014
@author: rockwotj
'''
import os

from google.appengine.api import users
import jinja2
import webapp2

import main
import models
from utils import user_utils


### Pages ###
class BasePage(webapp2.RequestHandler):
    """Page handlers should inherit from this one."""
    def get(self):
        user = users.get_current_user()
        if user_utils.is_validated(user):
            template = main.jinja_env.get_template(self.get_template())
            values = self.get_template_values()
            values["professors"] = models.Instructor.query().fetch(keys_only=True)
            values["classes"] = models.Course.query().fetch(keys_only=True)
            self.response.out.write(template.render(values))
        else:
            self.redirect(uri="/validate")

    def get_template_values(self):
        raise Exception("Subclasses must override this method")

    def get_template(self):
        raise Exception("Subclasses must override this method")


### Actions ###

class BaseAction(webapp2.RequestHandler):
    """ALL action handlers should inherit from this one."""
    def post(self):
        pass

    def get(self):
        pass

    def handle_post(self, player):
        raise Exception("Subclass must implement handle_post!")
