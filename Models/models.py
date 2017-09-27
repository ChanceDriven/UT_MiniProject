from google.appengine.ext import ndb


class Stream(ndb.Model):
    name = ndb.StringProperty()
    coverImgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.IntegerProperty()
    subscribers = ndb.IntegerProperty()

    def __init__(self, name="Stream1", subscribers=8, image_url="image.jpg"):
        ndb.Model.__init__(self)
        self.name = name
        self.subscribers = subscribers
        self.coverImgUrl = image_url


class Image(ndb.Model):
    streamId = ndb.StringProperty()
    imgUrl = ndb.StringProperty()
    updatedData = createdDate = ndb.DateTimeProperty(auto_now_add=True)

    def __init__(self, stream_id, image_url="image.jpg"):
        ndb.Model.__init__(self)
        self.streamId = stream_id
        self.image_url = image_url





