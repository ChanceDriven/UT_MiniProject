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
        self.images = []
        example_author = Author()
        self.author = example_author.put()

    def __str__(self):
        return self.name + '\t' + str(self.author)


class Image(ndb.Model):
    comments = ndb.StringProperty()
    updatedDate = createdDate = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.BlobProperty()

    def __init__(self, comments='', data=None):
        ndb.Model.__init__(self)
        # put image into google, get url
        self.comments = comments
        self.content = data


class EmailConfig(ndb.Model):
    reportFrequency = ndb.IntegerProperty()

    def __init__(self):
        ndb.Model.__init__(self)
        self.reportFrequency = 0
