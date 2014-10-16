from google.appengine.ext import ndb

class Course(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    overall_rating = ndb.FloatProperty(default=0.0)
    reviews = ndb.KeyProperty(kind=Review, repeated=True)
    taught_by = ndb.KeyProperty(kind=Instructor, repeated=True)

class Section(ndb.Model):
    term = ndb.KeyProperty(kind=Term)
    # class = ndb.KeyProperty(kind=Class) # Don't need to to parent Key?
    hour = ndb.StringProperty()
    instructor = ndb.KeyProperty(kind=Instructor)
    location = ndb.StringProperty()
    section = ndb.StringProperty()

class Review(ndb.Model):
    # Professor ratings
    helpfulness = ndb.IntegerProperty()
    clarity = ndb.IntegerProperty()
    instr_ease = ndb.IntegerProperty()
    # Class ratings
    grasp = ndb.IntegerProperty()
    workload = ndb.IntegerProperty()
    class_ease = ndb.IntegerProperty()
    comments = ndb.TextProperty()
    course = ndb.KeyProperty(kind=Course)
    instructor = ndb.KeyProperty(kind=Instructor)

class Term(ndb.Model):
    code = ndb.StringProperty()

class Instructor(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    overall_rating = ndb.FloatProperty(default=0.0)
    reviews = ndb.KeyProperty(kind=Review, repeated=True)
    classes = ndb.KeyProperty(kind=Course, repeated=True)
    department = ndb.StringProperty()
