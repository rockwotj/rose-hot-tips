"""
This module parses the 2014 Course Catalog File to get all the courses offered

Created on Sep 24, 2014.
@author: staszass.
"""

import csv
import logging
import sys

import main
import models
from utils import class_utils


class CourseFileParser:
	""" 
	A parser that pulls data from the 2014 Course Catalog File and parses it into
	a python class (course). Call the parse() method to get a list of all the courses.
	"""
	def __init__(self, csvfile):
		""" Creates a new CoursePageParser
		"""
		self.csvfile = csvfile
		self.courses = []

	def parse(self):
		""" Puts the CSV data into python classes """
		try:
			# Read all the rows as dictionaries with the first row being the header row and keys determined by column
			reader = csv.DictReader(utf_8_encoder(self.csvfile.splitlines()))
			for row in reader:
				current_course = Course(Title=row['COURSE_TITLE'], Dept=row['DEPT'], Number=row['COURSE_NUM'], Description=row['DESCRIPTION'])
				self.courses.append(current_course)

			return self.courses
		except:
			print sys.exc_info()[0]
			raise

class Course:
	""" The is the data structure for a course at Rose Hulman.
		Below are the fields of the struct:			
			Title: Course Title							Example: Introduction to Software Development
			Department: The department of the course	Example: CSSE
			Number: The course id number				Example: 120
			Description: The course description			Example: This course is an introduction...
	"""
	def __init__(self, Title, Dept="", Number="", Description=""):
		self.dept = Dept
		self.number = Number
		self.title = Title
		self.description = Description


def utf_8_encoder(unicode_csv_data):
	""" A generator that encodes the Unicode strings as UTF-8, one string (or row) at a time
	"""
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
		course_key = class_utils.get_course_key_from_course_id(course.dept + course.number)
		course_entity = models.Course(key=course_key,
									  dept=course.dept,
 									  number=course.number,
 									  title=course.title,
 									  description=course.description)
		course_entity.put()
	logging.info("Ended Parsing Course Information.")
