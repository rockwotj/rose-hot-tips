from google.appengine.ext import ndb


class User(ndb.Model):
    """ A user that knows if it they are verified as a valid Rose-Hulman user. """
    verified = ndb.BooleanProperty(default=False)

class Term(ndb.Model):
    """ A termcode for a class """
    code = ndb.StringProperty()

class Instructor(ndb.Model):
    """ An instructor that teaches a section of a course """
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    department = ndb.StringProperty()

class Course(ndb.Model):
    """ A course that Rose-Hulman offers during a year. """
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    #  We can't use these or we get circular dependancies
    # reviews = ndb.KeyProperty(kind=Review, repeated=True)
    # taught_by = ndb.KeyProperty(kind=Instructor, repeated=True)

class Section(ndb.Model):
    """ A section of a class that is being offered during a term. """
    # No class KeyProperty because it will be taken care of in the
    # parent key.
    term = ndb.KeyProperty(kind=Term)
    hour = ndb.StringProperty()
    instructor = ndb.KeyProperty(kind=Instructor)
    location = ndb.StringProperty()
    section = ndb.StringProperty()

class Review(ndb.Model):
    """ A review object that a user gives to a professor and a class. """
    # User parent key
    # Professor ratings
    helpfulness = ndb.IntegerProperty()
    clarity = ndb.IntegerProperty()
    instr_ease = ndb.IntegerProperty()
    # Class ratings
    grasp = ndb.IntegerProperty()
    workload = ndb.IntegerProperty()
    class_ease = ndb.IntegerProperty()
    # Other
    comments = ndb.TextProperty()
    # Keys to the courses
    course = ndb.KeyProperty(kind=Course)
    instructor = ndb.KeyProperty(kind=Instructor)




