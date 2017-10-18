import datetime
import json
from google.appengine.ext import ndb


class Author(ndb.Model):
    name = ndb.StringProperty()


class Stream(ndb.Model):
    name = ndb.StringProperty()
    author = ndb.KeyProperty()
    coverImgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.DateTimeProperty(repeated=True)
    subscribers = ndb.StringProperty(repeated=True)
    rank = ndb.IntegerProperty()
    view_count = ndb.ComputedProperty(lambda self: len(self.views))
    image_count = ndb.ComputedProperty(lambda self: len(self.images))
    tags = ndb.StringProperty(repeated=True)
    images = ndb.KeyProperty(repeated=True)

    def __init__(self, name="Stream1", subscribers=[], image_url="image.jpg", author=None, rank=99, tags=[]):
        ndb.Model.__init__(self)
        self.name = name
        self.subscribers = subscribers
        self.coverImgUrl = image_url
        self.rank = rank
        self.views = []
        self.tags = tags
        example_author = Author()
        self.author = example_author.put()

    def __str__(self):
        return self.name + '\t' + str(self.author) + '\nImages: ' + str(self.images)
    
    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class Image(ndb.Model):
    comments = ndb.StringProperty()
    updatedDate = createdDate = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.BlobProperty()

    def __init__(self, comments='', data=None):
        ndb.Model.__init__(self)
        # put image into google, get url
        self.comments = comments
        self.content = data
    
    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class EmailConfig(ndb.Model):
    reportFrequency = ndb.IntegerProperty()
    lastEmailSent = ndb.DateTimeProperty()
    def __init__(self):
        ndb.Model.__init__(self)
        self.reportFrequency = 0
        self.lastEmailSent = datetime.datetime.now()
    
    @property
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

#Note:Trying to create a Json encoder to handle more complex objects 
class CustomEncoder(json.JSONEncoder):
     def default(self, o):
         if isinstance(o, datetime.datetime):
             return {'__datetime__': o.replace(microsecond=0).isoformat()}
         return {"__{}__".format(o.__class__.__name__): o.__dict__}