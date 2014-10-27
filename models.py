from google.appengine.ext import ndb


class User(ndb.Model):
    """ A user that knows if it they are verified as a valid Rose-Hulman user. """
    # key contains email
    verified = ndb.BooleanProperty(default=False)

class Term(ndb.Model):
    """ A termcode for a class """
    # key contains termcode ie. 201410
    name = ndb.StringProperty()  # ie. Fall Quarter 2014-2015
    date_added = ndb.DateTimeProperty(auto_now_add=True)

class Instructor(ndb.Model):
    """ An instructor that teaches a section of a course """
    # key contains username ie. fisherds
    name = ndb.StringProperty()  # David Fisher

class Course(ndb.Model):
    """ A course that Rose-Hulman offers during a year. """
    # key contians courseID ie. CSSE120
    dept = ndb.StringProperty()  # ie. CSSE
    number = ndb.StringProperty()  # ie. 120
    title = ndb.StringProperty()  # ie. Intro to Software Development
    description = ndb.TextProperty()

class Section(ndb.Model):
    """ A section of a class that is being offered during a term. """
    # parent contains the Course Key
    # key is a generated random integer (Don't put the field in on construction)
    term = ndb.KeyProperty(kind=Term)
    hour = ndb.StringProperty()  # ie. 3-7:8
    instructor = ndb.KeyProperty(kind=Instructor, repeated=True)
    location = ndb.StringProperty()  # ie. O257:M225
    section = ndb.StringProperty()  # ie. 01
    full_title = ndb.ComputedProperty(lambda self: self.key.parent().string_id() + "-" + self.section)

    @property
    def instructors(self):
        return self.instructor

class Review(ndb.Model):
    """ A review object that a user gives to a professor and a class. """
    # parent contains the User Key
    # All ratings on a scale from 1-5?
    # Professor ratings
    helpfulness = ndb.IntegerProperty()
    clarity = ndb.IntegerProperty()
    instr_ease = ndb.IntegerProperty()
    # Class ratings
    grasp = ndb.IntegerProperty()
    workload = ndb.IntegerProperty()
    class_ease = ndb.IntegerProperty()
    # Other
    date_added = ndb.DateTimeProperty(auto_now_add=True)
    comments = ndb.TextProperty()
    # Keys to the course & prof
    course = ndb.KeyProperty(kind=Course)
    instructor = ndb.KeyProperty(kind=Instructor)




