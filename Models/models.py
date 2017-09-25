from google.appengine.ext import ndb


class Stream(ndb.Model):
    id = ndb.IntProperty()
    author = ndb.UserProperty()
    imgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.IntProperty()
    name = ndb.StringProperty()

    def __init__(self):
        self.name = 'Stream1'
        self.author = ndb.UserProperty()
        self.subscribers = []
        self.imageUrl = 'image.jpg'
        self.createdDate = ndb.DateTimeProperty(auto_now_add=True)

    def __init__(self, name, author, subscribers, image_url):
        self.name = name
        self.author = author
        self.subscribers = subscribers
        self.imageUrl = image_url
        self.createdDate = ndb.DateTimeProperty(auto_now_add=True)
