"""
TODO: Describe this script

Created on Sep 24, 2014.
@author: rockwotj.
"""

import csv
import logging

import main


class CourseFileParser:
	pass

def run():
	""" The function that will be called put the course data into the Datastore. """
	logging.info("Started Parsing Course Information from CSV file.")
	csvfile = main.jinja_env.get_template("templates/2014_course_catalog.csv").render()
	parser = CourseFileParser()
	# TODO: Parse the csvFile and put it's data into Course Entities from models.py
	logging.info("Ended Parsing Course Information.")
