#README

mongo_orm is a simple, lightweight object relation mapper for MongoDB, based on Django's default ORM.  It's goal is to provide a super easy way to start using MongoDB in any Python project.

#Getting Started

A functioning example is found in test.py.  These are the basic steps to get mongo_orm working in your project.

1) Define you database settings in db_settings.py

2) Define you models in any file by importing models.py and creating Objects like the one found in test.py.  Mainly, this means creating an object with a 'fields' method, containing all the data fields you'd like to save.

#Usage

If we have a model class named 'TestModel':

    # Create a new object and give it some data
    test = TestModel()
	test.normal_string = "Hello."
	test.normal_int = 100
	
	# Save the object to Mongo
	test.save()

	# Fetch the object we just saved
	print str(TestModel.objects().get(_id=test.uid))

	# List everything in the TestModel collection 
	for item in TestModel.objects().all():
	    print str(item)