import models


class TestModel(models.Model):
    def fields(self, **kwargs):
        self.normal_string = models.CharField(**kwargs)
        self.string_with_default = models.CharField(default="this is a default", **kwargs)
        self.normal_int = models.IntegerField(**kwargs)
        
    def __unicode__(self):
        return "%s (%s)" % (self.normal_string, self.uid)
       
           
test = TestModel()
test.normal_string = "Hello."
test.normal_int = 100
test.save()

print
print str(TestModel.objects().get(_id=test.uid))
print

for item in TestModel.objects().all():
    print str(item)
    print item.normal_int
