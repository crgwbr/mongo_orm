#!/usr/bin/python
"""
@author Craig Weber
Sample implementation of mongo_orm
"""

import models

"""
This is a sample model class.  The important parts
to notice here are the fields method (required for each 
model) and the transmission of '**kwargs' from the fields 
method to each individual field.
"""
class TestModel(models.Model):
    def fields(self, **kwargs):
        self.normal_string = models.CharField(**kwargs)
        self.string_with_default = models.CharField(default="this is a default", **kwargs)
        self.normal_int = models.IntegerField(**kwargs)
        
    def __unicode__(self):
        return "%s (%s)" % (self.normal_string, self.uid)
       

# Create a new object, set some attributes, and save to the db          
test = TestModel()
test.normal_string = "Hello."
test.normal_int = 100
test.save()

# Fetch the object we just saved
print str(TestModel.objects().get(_id=test.uid))


# List everything in the db
for item in TestModel.objects().all():
    print str(item)
