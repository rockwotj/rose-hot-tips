'''
Created on Oct 21, 2014
@author: rockwotj
'''

from google.appengine.api import users
from google.appengine.ext import deferred
import webapp2

import base_handler
import main
import models
from scripts import section_script, course_script
from utils import class_utils


class LandingPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/landingPage.html"

    def get_template_values(self, user):
        return {"terms": models.Term.query().order(-models.Term.date_added)}

class UserPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/userProfile.html"

    def get_template_values(self, user):
        return {}

class CoursePageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/coursePage.html"

    def get_template_values(self, user):
        urlsafe = self.request.get("id")
        return {}

class ProfessorPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/professorPage.html"

    def get_template_values(self, user):
        urlsafe = self.request.get("id")
        return {}

class ResultsPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/resultPage.html"

    def get_template_values(self, user):
        query = self.request.get("q")
        termcode = self.request.get("termcode")
        termcode_key = class_utils.get_term_key_from_code(termcode)
        results = models.Section.query(models.Section.term == termcode_key)
        return {"results":results}

class ReviewHandler(base_handler.BaseAction):
    def post(self):
        base_handler.BaseAction.post(self)

class ValidatePageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/validateUser.html"

    def get_template_values(self, user):
        return {}

class AdminUpdateHandler(webapp2.RedirectHandler):
    def get(self):
        if users.is_current_user_admin():
            template = main.jinja_env.get_template("templates/admin.html")
            self.response.write(template.render({}))
        else:
            self.redirect(uri="/")

    def post(self):
        if users.is_current_user_admin():
            if self.request.get("parse_courses"):
                deferred.defer(course_script.run)
            else:
                username = self.request.get("username")
                password = self.request.get("password")
                termcode = self.request.get("termcode")
                deferred.defer(section_script.run, username, password, termcode)
            self.redirect(uri=self.request.referer)
        else:
            self.redirect(uri="/")

sitemap = [("/", LandingPageHandler),
           ("/result", ResultsPageHandler),
           ("/me", UserPageHandler),
           ("/course", CoursePageHandler),
           ("/professor", ProfessorPageHandler),
           ("/review", ReviewHandler),
           ("/validate", ValidatePageHandler),
           ("/admin", AdminUpdateHandler)]
