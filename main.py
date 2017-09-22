from google.appengine.ext import db
from google.appengine.api import users
import webapp2


class Stream(db.Model):
    id = db.IntProperty()
    author = db.UserProperty()
    imgUrl = db.StringProperty()
    createdDate = db.DateTimeProperty(auto_now_add=True)
    views = db.IntProperty()


class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')


class Login(webapp2.RequestHandler):
    def post(self, user_id):
        # Need to return a session ID instead
        self.response.write(user_id)


class StreamRest(webapp2.RequestHandler):
    def get(self):
        # all streams
        all_streams = db.GqlQuery("select * from streams")
        self.response.write(all_streams)

    def get(self, stream_id):
        stream = db.GqlQuery("select * from streams "
                             "where id = :1", stream_id)
        self.response.write(stream)


class StreamTrending(webapp2.RequestHandler):
    def get(self):
        # change out with trending streams
        all_streams = db.GqlQuery("select * from streams "
                                  "where rownum < 11 "
                                  "orderby views desc")
        self.response.write(all_streams)


class Management(webapp2.RequestHandler):
    def get(self, user_id):
        subscribed = db.GqlQuery("select a.* from streams a, subscriptions b "
                                 "where b.author = :1 and a.id = b.streamId", user_id)
        authored = db.GqlQuery("select * from streams "
                               "where author = :1", user_id)
        self.response.write(subscribed, authored)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/(\w+)', Login),
    (r'/streams', StreamRest),
    (r'/streams/(\w+)', StreamRest)
], debug=True)
