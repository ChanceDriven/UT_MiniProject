from google.appengine.ext import ndb


class Stream(ndb.Model):
    name = ndb.StringProperty()
    coverImgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.IntegerProperty()
    subscribers = ndb.IntegerProperty()
    imgUrls = ndb.StringProperty(repeated=True)

    def __init__(self, name="Stream1", subscribers=8, image_url="image.jpg"):
        ndb.Model.__init__(self)
        self.name = name
        self.subscribers = subscribers
        self.coverImgUrl = image_url


class Image(ndb.Model):
    name = ndb.StringProperty()
    updatedDate = createdDate = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.BlobProperty()

    def __init__(self, name, data=None):
        ndb.Model.__init__(self)
        # put image into google, get url
        self.name = name
        self.content = data
