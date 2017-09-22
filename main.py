from google.appengine.ext import db
from google.appengine.api import users
import webapp2


class Stream(db.Model):
    id = db.IntProperty()
    author = db.UserProperty()
    imgUrl = db.StringProperty()
    createdDate = db.DateTimeProperty(auto_now_add=True)


class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello, webapp2!')


class Login(webapp2.RequestHandler):
    def post(self, user_id):
        #Need to return a session ID instead
        self.response.write(user_id)


class Management(webapp2.RequestHandler):
    def get(self, user_id):
        subscribed = db.GqlQuery("select a.* from streams a, subscriptions b "
                                 "where b.author = :1 and a.id = b.streamId", user_id)
        authored = db.GqlQuery("select * from streams "
                               "where author = :1", user_id)
        self.response.write(subscribed, authored)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/(\w+)', Login)
], debug=True)
