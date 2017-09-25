from google.appengine.ext import ndb


class Stream(ndb.Model):
    imgUrl = ndb.StringProperty()
    createdDate = ndb.DateTimeProperty(auto_now_add=True)
    views = ndb.IntegerProperty()
    name = ndb.StringProperty()
    subscribers = ndb.IntegerProperty()

    def __init__(self):
        pass
