"""
TODO: Describe this script

Created on Sep 24, 2014.
@author: rockwotj.
"""

import csv
import logging
import sys

import main
import models


class CourseFileParser:
	
	def __init__(self, csvfile):
		self.csvfile = csvfile
		self.courses = []
	
	def parse(self):
		try:
			reader = csv.DictReader(utf_8_encoder(self.csvfile.splitlines()))
			for row in reader:
				current_course = Course(Title=row['COURSE_TITLE'],Dept=row['DEPT'],Number=row['COURSE_NUM'], Description=row['DESCRIPTION'])
				self.courses.append(current_course)
			
			return self.courses
		except:
			print sys.exc_info()[0]
			raise

class Course:
	
	def __init__(self, Title, Dept="", Number="", Description=""):
		self.dept = Dept
		self.number = Number
		self.title = Title
		self.description = Description
		

def utf_8_encoder(unicode_csv_data):
	for line in unicode_csv_data:
		yield line.encode('utf-8')	

def run():
	""" The function that will be called put the course data into the Datastore. """
	logging.info("Started Parsing Course Information from CSV file.")
	csvfile = main.jinja_env.get_template("templates/2014_course_catalog.csv").render({})
	parser = CourseFileParser(csvfile)
	courses = parser.parse()
	logging.info(str(len(courses)) + " courses found")
 	for course in courses:
 		course_entity = models.Course(dept=course.dept,
 									number=course.number,
 									title=course.title,
 									description=course.description)
 		course_entity.put()
	logging.info("Ended Parsing Course Information.")