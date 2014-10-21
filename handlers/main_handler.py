'''
Created on Oct 21, 2014
@author: rockwotj
'''
import os

import jinja2
import webapp2


jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

class LandingPageHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/landingPage.html")
        self.response.write(template.render({}))

sitemap = [("/", LandingPageHandler)]