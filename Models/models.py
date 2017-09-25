from google.appengine.ext import db


class Stream(db.Model):
    id = db.IntProperty()
    author = db.UserProperty()
    imgUrl = db.StringProperty()
    createdDate = db.DateTimeProperty(auto_now_add=True)
    views = db.IntProperty()
    name = db.StringProperty()

    def __init__(self):
        self.name = 'Stream1'
        self.author = db.UserProperty()
        self.subscribers = []
        self.imageUrl = 'image.jpg'
        self.createdDate = db.DateTimeProperty(auto_now_add=True)

    def __init__(self, name, author, subscribers, image_url):
        self.name = name
        self.author = author
        self.subscribers = subscribers
        self.imageUrl = image_url
        self.createdDate = db.DateTimeProperty(auto_now_add=True)
