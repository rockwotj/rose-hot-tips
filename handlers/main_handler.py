'''
Created on Oct 21, 2014
@author: rockwotj
'''

from google.appengine.api import users
from google.appengine.ext import deferred, ndb
import webapp2

import base_handler
import main
from models import Review
from scripts import section_script, course_script
from utils import class_utils, user_utils


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

    def post(self):
        new_review = Review(parent=user_utils.get_user_key(users.get_current_user()),
                            instructor=class_utils.get_instructor_key("prof_name"),
                            course=class_utils.get_course_key("class_id"),
                            helpfulness=int(self.request.get("helpfulness")),
                            clarity=int(self.request.get("clarity")),
                            instr_ease=int(self.request.get("p_ease")),
                            grasp=int(self.request.get("grasp")),
                            workload=int(self.request.get("workload")),
                            class_ease=int(self.request.get("c_ease")),
                            comments=self.request.get("comments"))
        new_review.put()
        self.redirect(self.request.referer)

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
