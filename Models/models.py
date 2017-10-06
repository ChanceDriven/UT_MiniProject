import datetime
from google.appengine.ext import ndb


class Stream(ndb.Model):
    name = ndb.StringProperty()
    author = ndb.StringProperty()
    coverImgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.DateTimeProperty(repeated=True)
    subscribers = ndb.StringProperty(repeated=True)
    rank = ndb.IntegerProperty()
    view_count = ndb.ComputedProperty(lambda self: len(self.views))
    tags = ndb.StringProperty(repeated=True)
    images = ndb.StringProperty(repeated=True)

    def __init__(self, name="Stream1", subscribers=[], image_url="image.jpg", author="", rank=99, tags=[]):
        ndb.Model.__init__(self)
        self.name = name
        self.subscribers = subscribers
        self.coverImgUrl = image_url
        self.author = author
        self.rank = rank
        self.views = []
        self.views = []
        self.tags = tags
        self.images = []


class Image(ndb.Model):
    comments = ndb.StringProperty()
    updatedDate = createdDate = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.BlobProperty()

    def __init__(self, comments, data=None):
        ndb.Model.__init__(self)
        # put image into google, get url
        self.comments = comments
        self.content = data


class EmailConfig(ndb.Model):
    reportFrequency = ndb.IntegerProperty()
    lastEmailSent = ndb.DateTimeProperty()
    def __init__(self):
        ndb.Model.__init__(self)
        self.reportFrequency = 0
        self.lastEmailSent = datetime.datetime.now()

