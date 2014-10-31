'''
Created on Oct 21, 2014
@author: rockwotj
'''

from google.appengine.api import users
from google.appengine.ext import deferred
import webapp2

import base_handler
import main
from scripts import section_script, course_script
from utils import class_utils

### Normal Pages ###

class LandingPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/landingPage.html"

    def get_template_values(self, user):
        terms = class_utils.get_all_termcodes()
        return {"terms": terms }

class UserPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/userProfile.html"

    def get_template_values(self, user):
        return {}

class CoursePageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/coursePage.html"

    def get_template_values(self, user):
        course_id = self.request.get("id")
        course = class_utils.get_course_key(course_id).get()
        return {"course":course}

class ProfessorPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/professorPage.html"

    def get_template_values(self, user):
        username = self.request.get("id")
        prof = class_utils.get_instructor_key(username).get()
        return {"professor":prof}

class ResultsPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/resultPage.html"

    def get_template_values(self, user):
        query = self.request.get("q")
        termcode = self.request.get("termcode")
        if query:
            results = class_utils.search_for_sections(query, termcode)
        else:
            results = class_utils.get_all_sections(termcode)
        return {"results":results}

class ReviewHandler(base_handler.BaseAction):
    """ TODO! """

    def post(self):
        base_handler.BaseAction.post(self)

class ValidatePageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/validateUser.html"

    def get_template_values(self, user):
        return {}

### Special Pages ###

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

### Sitemap ###

sitemap = [("/", LandingPageHandler),
           ("/result", ResultsPageHandler),
           ("/me", UserPageHandler),
           ("/course", CoursePageHandler),
           ("/professor", ProfessorPageHandler),
           ("/review", ReviewHandler),
           ("/validate", ValidatePageHandler),
           ("/admin", AdminUpdateHandler)]
