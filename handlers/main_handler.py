'''
Created on Oct 21, 2014
@author: rockwotj
'''

from google.appengine.api import users
from google.appengine.ext import deferred
import webapp2

import base_handler
import main
from scripts import section_scripts
import logging


class LandingPageHandler(base_handler.BasePage):
    def get_template(self):
        logging.info("Opening main page")
        return "templates/landingPage.html"
    def get_template_values(self):
        return {}

def update_section_data(username, password, termcode):
    section_scripts.run(username, password, termcode)

class AdminUpdateHandler(webapp2.RedirectHandler):
    def get(self):
        if users.is_current_user_admin():
            template = main.jinja_env.get_template("templates/admin.html")
            self.response.write(template.render({}))
        else:
            self.redirect(uri="/")


    def post(self):
        if users.is_current_user_admin():
            username = self.request.get("username")
            password = self.request.get("password")
            termcode = self.request.get("termcode")
            deferred.defer(update_section_data, username, password, termcode)
            self.redirect(uri=self.request.referer)
        else:
            self.redirect(uri="/")


sitemap = [("/", LandingPageHandler), ("/admin", AdminUpdateHandler)]
