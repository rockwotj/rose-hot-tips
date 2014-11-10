'''
Created on Oct 21, 2014
@author: rockwotj
'''

from google.appengine.api import users
from google.appengine.ext import deferred, ndb
import webapp2

import base_handler
import main
import models
from scripts import section_script, course_script
from utils import class_utils, user_utils


### Normal Pages ###
class LandingPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/landingPage.html"

    def get_template_values(self):
        terms = class_utils.get_all_termcodes()
        return {"terms": terms }

class UserPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/userProfile.html"

    def get_template_values(self):
        return {}

class CoursePageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/coursePage.html"

    def get_template_values(self):
        course_id = self.request.get("id")
        course_key = class_utils.get_course_key(course_id)
        reviews = class_utils.get_course_reviews_from_key(course_key)
        values = {"course":course_key.get(), "reviews":reviews}
        values['overall_rating'] = 0
        values['grasp_rating'] = 0
        values['workload_rating'] = 0
        values['ease_rating'] = 0
        count = 0.0
        for review in reviews:
            values['overall_rating'] += (review.grasp + review.workload + review.class_ease) / 3
            values['grasp_rating'] += review.grasp
            values['workload_rating'] += review.workload
            values['ease_rating'] += review.class_ease
            count += 1.0
        if count > 0:
            values['overall_rating'] /= count
            values['grasp_rating'] /= count
            values['workload_rating'] /= count
            values['ease_rating'] /= count
        else:
            values['overall_rating'] = "N/A"
            values['grasp_rating'] = "N/A"
            values['workload_rating'] = "N/A"
            values['ease_rating'] = "N/A"
        return values

class ProfessorPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/professorPage.html"

    def get_template_values(self):
        username = self.request.get("id")
        prof_key = class_utils.get_instructor_key(username)
        reviews = class_utils.get_instructor_reviews_from_key(prof_key)
        values = {"professor":prof_key.get(), "reviews":reviews}
        values['overall_rating'] = 0
        values['helpfulness_rating'] = 0
        values['clarity_rating'] = 0
        values['ease_rating'] = 0
        count = 0.0
        for review in reviews:
            values['overall_rating'] += (review.helpfulness + review.clarity + review.instr_ease) / 3
            values['helpfulness_rating'] += review.helpfulness
            values['clarity_rating'] += review.clarity
            values['ease_rating'] += review.instr_ease
            count += 1.0
        if count > 0:
            values['overall_rating'] /= count
            values['helpfulness_rating'] /= count
            values['clarity_rating'] /= count
            values['ease_rating'] /= count
        else:
            values['overall_rating'] = "N/A"
            values['helpfulness_rating'] = "N/A"
            values['clarity_rating'] = "N/A"
            values['ease_rating'] = "N/A"
        return values
        return {}

class ResultsPageHandler(base_handler.BasePage):
    def get_template(self):
        return "templates/resultPage.html"

    def get_template_values(self):
        query = self.request.get("q")
        termcode = self.request.get("termcode")
        if query:
            results = class_utils.search_for_sections(query, termcode)
        else:
            results = class_utils.get_all_sections(termcode)
        return {"results":results}

class ReviewHandler(base_handler.BaseAction):

    def post(self):
        new_review = models.Review(parent=user_utils.get_user_key(users.get_current_user()),
                            instructor=class_utils.get_instructor_key(self.request.get("prof_name")),
                            course=class_utils.get_course_key(self.request.get("class_name")),
                            helpfulness=int(self.request.get("helpfulness")),
                            clarity=int(self.request.get("clarity")),
                            instr_ease=int(self.request.get("p_ease")),
                            grasp=int(self.request.get("grasp")),
                            workload=int(self.request.get("workload")),
                            class_ease=int(self.request.get("c_ease")),
                            comments=self.request.get("comments"))
        new_review.put()
        self.redirect(self.request.referer)
    
    def deleteTip(self):
        review_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        review_key.delete()
        self.redirect(self.request.referer)

### Special Pages ###

class ValidatePageHandler(webapp2.RedirectHandler):
    def get(self):
        user = users.get_current_user()
        if user_utils.is_validated(user):
            self.redirect(uri="/")
        else:
            template = main.jinja_env.get_template("templates/validateUser.html")
            self.response.out.write(template.render({"Validate":True}))

    def post(self):
        user = users.get_current_user()
        valid = user_utils.validate_user(self.request.get("username"), self.request.get("password"))
        user_utils.set_validate(user, valid)
        if valid:
            self.redirect(uri="/")
        else:
            self.redirect(uri="/validate")

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
