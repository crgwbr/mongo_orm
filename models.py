from pymongo import *
from db_settings import *
import re

# Init Connection to MongoDB
connection = Connection(HOST, PORT)
db = connection[DB]


# Query Object    
class Query():
    def __init__(self, model, filters={}):
        self.collection_name = model.__name__
        self.model = model
        self.collection = db[self.collection_name]
        self.filters = filters
            
    def get(self, **kwargs):
        return self.filter(**kwargs).one()
       
    def filter(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.filters[key] = value
        return self
        
    def all(self):
        results = self.collection.find(self.filters)
        self.filters = {}
        mapped = []
        for result in results:
            obj = self.model()
            obj.load(result)
            mapped.append(obj)
        return mapped
        
    def one(self):
        result = self.collection.find_one(self.filters)
        self.filters = {}
        obj = self.model()
        obj.load(result)
        return obj
        
        
# Main Model Base Class
class Model():
    def __init__(self, *args, **kwargs):
        # Init Fields
        self.uid = None
        self.collection = db[self.__class__.__name__]
        self.fields(get_validator=False)
        self.validators = None
        
    @classmethod
    def objects(self):
        return Query(self, {})
        
    def load(self, query_result):
        for key, value in query_result.iteritems():
            self.__dict__[key] = value
        self.uid = query_result['_id']
    
    def get_field_validators(self):
        if not self.validators:
            self.validators = self.__class__()
            self.validators.fields(get_validator=True)
            
        validators = {}
        for key, value in self.validators.__dict__.iteritems():
            try:
                if value.is_model_field and key != "collection":
                    validators[key] = value
            except:
                pass
        return validators
        
    def get_fields(self):
        fields = {}
        for key, value in self.get_field_validators().iteritems():
            try:
                if value.is_model_field and key != "collection":
                    fields[key] = self.__dict__[key]
            except:
                pass
        return fields
       
    def is_valid(self):
        field_validators = self.get_field_validators()
        fields = self.get_fields()
        for name, validator in field_validators.iteritems():
            if not validator.is_valid(value=fields[name]):
                return False
        return True
        
    def save(self):
        if self.is_valid():
            data = self.get_fields()
            if self.uid == None:
                uid = self.collection.insert(data)
                self.uid = uid
            else:
                data["_id"] = self.uid
                self.collection.update({"_id": self.uid}, data)
        else:
            raise Exception("Model is not valid")
            
    def __str__(self):
        return self.__unicode__()


# Base Validator Class
class MetaFieldBase():
    def __init__(self, *args, **kwargs):
        self.is_model_field = True
        self.value = kwargs.get("value")
        self.options = kwargs
        
        
"""
Char Field
kwarg options:
  - default
  - max_length
  - min_length
  - match_regex
"""
class CharField(str):
    def __new__(cls, *args, **kwargs):
        if kwargs.get('get_validator'):
            return CharFieldMeta(*args, **kwargs)
        else:
            # If default is a string, return it
            # If not, its probable a function, so return the result
            default = kwargs.get("default", "")
            if type(default) == str:
                return default
            else:
                return default()
        
class CharFieldMeta(MetaFieldBase):
    def is_valid(self, value=None):
        if value:
            self.value = value
        
        valid = True
        # Setup Validation Rules
        # Null is special
        if self.options.get("null") and self.value == None:
            return True
        elif self.value == None:
            return False

        # If any of these are False, valid = False
        rules = (
            bool(type(self.value) == str),
            bool(not self.options.get("max_length")  or len(self.value) < self.options["max_length"]),
            bool(not self.options.get("min_length")  or len(self.value) > self.options["min_length"]),
            bool(not self.options.get("match_regex") or re.match(self.options['match_regex'], self.value)),
        )
        # Loop through the rules
        for rule in rules:
            if not rule:
                return False
                
        # Must be valid
        return True
        
        
"""
IntegerField Field
kwarg options:
  - default
  - max
  - min
"""
class IntegerField(int):
    def __new__(cls, *args, **kwargs):
        if kwargs.get('get_validator'):
            return IntegerFieldMeta(*args, **kwargs)
        else:
            # If default is a string, return it
            # If not, its probable a function, so return the result
            default = kwargs.get("default", 0)
            if type(default) == int:
                return default
            else:
                return default()

class IntegerFieldMeta(MetaFieldBase):
    def is_valid(self, value=None):
        if value:
            self.value = value

        valid = True
        # Setup Validation Rules
        # Null is special
        if self.options.get("null") and self.value == None:
            return True
        elif self.value == None:
            return False

        # If any of these are False, valid = False
        rules = (
            bool(type(self.value) == int),
            bool(not self.options.get("max") or self.value < self.options["max"]),
            bool(not self.options.get("min") or self.value > self.options["min"]),
        )
        # Loop through the rules
        for rule in rules:
            if not rule:
                return False

        # Must be valid
        return True

