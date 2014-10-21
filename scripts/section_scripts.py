"""
This module pulls data from https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl
To get the classes for Rose-Hulman


Created on Sep 24, 2014.
@author: rockwotj.
"""

from HTMLParser import HTMLParser
import logging
import re
import urllib2


class SectionPageParser:
	""" 
	A parser that pulls data off of the schedule pages at Rose and parses it into
	a python class (section). Call the parse() method to get a list of all the sections.
	 """
	# class attributes
	url = "https://prodweb.rose-hulman.edu/regweb-cgi/reg-sched.pl"

	# The states of the FSM for the HTML_FiniteStateMachine
	START_STATE = 0
	START_ROW = 1
	FIND_CRN = 2
	FIND_TITLE = 3
	FIND_INSTR = 4
	FIND_SCHEDULE = 5
	END_ROW = 6

	def __init__(self, termcode, username, password):
		""" Creates a new SectionPageParser that pulls data off of the Rose-Hulman Schedule look-up page 
			Need to pass in the termcode (i.e. 201510) to get the sections for that term and
			a KERBEROS username and password to pull the data into the database.
		"""
		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# add the password for the URL
		password_mgr.add_password(None, SectionPageParser.url, username, password)
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		# create private class variable "__opener" (OpenerDirector instance)
		self.__opener = urllib2.build_opener(handler)

		# placeholder for the list of classes from the schedule page
		self.sections = []

		# placeholder for the memoize dictionary of professor's username and full names
		self.__professors = {}

		self.termcode = termcode

	def __get_schedule_html(self):
		""" PRIVATE: Gets the HTML data that is the courses offered for a given quarter """
		# use the __opener to fetch a URL
		args = "termcode=" + SectionPageParser.term_code + "&view=table&id1=&id4=*&bt4=Room&id5="
		html_string = self.__opener.open(SectionPageParser.url, data=args).read()
		# replace all of the '&' with '+' so that the parser works correctly.
		return html_string.replace("&", "+")

	def __parse_html(self, html):
		""" PRIVATE: Puts the HTML Data into python classes """
		parser = SectionPageParser.HTML_FiniteStateMachine(self)
		parser.feed(html)

	def parse(self):
		""" The method that parses the schedule page for you. """
		self.__parse_html(self.__get_schedule_html())
		return self.sections

	def get_professor_name(self, usr_id):
		""" 
		This method takes a professor's KEBEROS username and returns their full name 
		Example:
			SectionPageParser.get_professor_name("boutell") # returns: 'Matthew R Boutell'
		"""
		# Memoized to improve performance and reduce the number of page requests.
		if usr_id in self.__professors:
			return self.__professors[usr_id]
		else:
			try:
				args = "?type=Instructor&termcode=" + SectionPageParser.term_code + "&view=table&id=" + usr_id
				html = self.__opener.open(SectionPageParser.url + args).read()
				profname = re.search("Name: .*?<", html).group()[6:-1]
				self.__professors[usr_id] = profname
				return profname
			except:
				return None

	class HTML_FiniteStateMachine(HTMLParser):
		""" Inner class to handle the actual parsing of the data in the schedule page """

		def __init__(self, schedule_page_parser):
			HTMLParser.__init__(self)
			self.__current_state = SectionPageParser.START_STATE
			self.__parent = schedule_page_parser
			self.__current_section = None
			self.__parent.sections = []
			self.__counter = 0

		def handle_starttag(self, tag, attrs):
			tag = tag.lower()
			if self.__current_state == SectionPageParser.START_STATE:
				if tag == "table":
					self.__counter += 1
				elif tag == "tr" and self.__counter == 2:
					self.__current_state = SectionPageParser.START_ROW
			elif self.__current_state == SectionPageParser.START_ROW:
				if tag == "a":
					self.__current_state = SectionPageParser.FIND_CRN
			elif self.__current_state == SectionPageParser.FIND_CRN:
				pass
			elif self.__current_state == SectionPageParser.FIND_TITLE:
				if tag == "a":
					self.__current_state = SectionPageParser.FIND_INSTR
			elif self.__current_state == SectionPageParser.FIND_INSTR:
				pass
			elif self.__current_state == SectionPageParser.FIND_SCHEDULE:
				if tag == "td":
					self.__counter += 1
			elif self.__current_state == SectionPageParser.END_ROW:
				pass
			else:
				pass

		def handle_data(self, data):
			# There was some kind of problem with the data cutting off after
			# a '&' so I changed them to '+' and am changing them back here
			data = data.replace("+", "&")
			if self.__current_state == SectionPageParser.START_STATE:
				pass
			elif self.__current_state == SectionPageParser.START_ROW:
				pass
			elif self.__current_state == SectionPageParser.FIND_CRN:
				index = data.rfind("-")
				self.__current_section = section(CID=data[:index], CRN=data)
				self.__current_state = SectionPageParser.FIND_TITLE
				self.__counter = 0
			elif self.__current_state == SectionPageParser.FIND_TITLE:
				self.__counter += 1
				if self.__counter == 2:
					self.__current_section.title = data
			elif self.__current_state == SectionPageParser.FIND_INSTR:
				self.__current_section.iid = data
				if data.count("&") == 0:
					self.__current_section.instructor = self.__parent.get_professor_name(data)
				elif data.count("&") == 1:
					index = data.index("&")
					instr1 = self.__parent.get_professor_name(data[:index]) + " & "
					self.__current_section.instructor = instr1 + self.__parent.get_professor_name(data[index + 1:])
				else:
					self.__current_section.instructor = "Many Instructors"
				self.__current_state = SectionPageParser.FIND_SCHEDULE
				self.__counter = 0
			elif self.__current_state == SectionPageParser.FIND_SCHEDULE:
				if self.__counter == 4:
					if data.count("/") == 0:
						self.__current_section.time = data
						self.__current_section.location = data
						self.__current_state = SectionPageParser.END_ROW
					else:
						data = data.split(":")
						times = []
						rooms = []
						for d in data:
							index = d.rfind("/")
							times.append(d[:index])
							rooms.append(d[index + 1:])
						self.__current_section.time = ":".join(times)
						self.__current_section.location = ":".join(rooms)
						self.__current_state = SectionPageParser.END_ROW
			elif self.__current_state == SectionPageParser.END_ROW:
				pass
			else:
				pass

		def handle_endtag(self, tag):
			tag = tag.lower()
			if self.__current_state == SectionPageParser.START_STATE:
				pass
			else:
				if tag == "tr" and self.__current_section != None:
					self.__parent.sections.append(self.__current_section)
					# print self.__parent.sections[-1]  # UNCOMMENT HERE TO SEE THE CLASSES APPEAR AS THEY ARE PARSED
					self.__current_section = None
					self.__current_state = SectionPageParser.START_ROW

class section:
	""" The is the data structure for a class section at Rose Hulman.
		Below are the fields of the struct:			
			CID: The course id number				  	Example: CSSE120
			CRN: The number & section of a course.	 	Example: CSSE120-01
			Title: Course Title							Example: Introduction to Software Development
			IID: The usr name of a prof					Example: boutell
			Instructor: Full name of prof			  	Example: Matthew R Boutell 
			Time: hour(s) and days of the class			Example: MTR/8:W/5-7
			Location: Which room the class is in	   	Example: O257:O159	  """

	def __init__(self, CID, CRN, Title="", IID="", Instructor="", Time="", Location=""):
		self.cid = CID
		self.crn = CRN
		self.title = Title
		self.iid = IID
		self.instructor = Instructor
		self.time = Time
		self.location = Location

	def __str__(self):
		# loop through the values of __dict__ calling str? Not in order then...
		return 	str(self.cid) + "|" + str(self.crn) + "|" + \
				str(self.title) + "|" + str(self.iid) + "|" + \
				str(self.instructor) + "|" + str(self.time) + \
				"|" + str(self.location)


#-----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
#-----------------------------------------------------------------------
def run(username, password, termcode):
	try:
		parser = SectionPageParser(termcode, username, password)
		logging.info("Started Parsing " + termcode + " Section Information for " + username)
		sections = parser.parse()
	except:
		logging.error("Error loading webpage")
		return
	for section in sections:
		pass
	logging.info("Ended Parsing Section Information")
