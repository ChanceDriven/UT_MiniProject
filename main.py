import os

from google.appengine.ext import ndb

import jinja2
import webapp2
from services import services

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


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
        all_streams = services.get_all_streams()
        template = JINJA_ENVIRONMENT.get_or_select_template('/views/all_streams.html').render(all_streams)
        self.response.write(template)

class StreamTrending(webapp2.RequestHandler):
    def get(self):
        # change out with trending streams
        all_streams = ndb.GqlQuery("select * from streams "
                                   "where rownum < 11 "
                                   "orderby views desc")
        self.response.write(all_streams)


class StreamSearch(webapp2.RequestHandler):
    def get(self, query):
        # change out with trending streams
        all_streams = ndb.GqlQuery("select * from streams "
                                   "where name % :1 ", query)
        self.response.write(all_streams)


class Management(webapp2.RequestHandler):
    def get(self, user_id):
        subscribed = ndb.GqlQuery("select a.* from streams a, subscriptions b "
                                  "where b.author = :1 and a.id = b.streamId", user_id)
        authored = ndb.GqlQuery("select * from streams "
                                "where author = :1", user_id)
        self.response.write(subscribed, authored)


class CreateStream(webapp2.RequestHandler):
    # Handler to create the stream information should be passed to the service to create
    # the object and store it.
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/create_stream.html')
        services.Service.create_stream("test", 5, "test2")
        self.response.write(template)

    def post(self):
        pass

class Error(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/error.html').render()
        self.response.write(template)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/(\w+)', Login),
    (r'/streams', StreamRest),
    (r'/streams/(\w+)', StreamRest),
    (r'/create-stream', CreateStream),
    (r'/streams/trending', StreamTrending),
    (r'/streams/search/(\w+)', StreamSearch),
    (r'/error', Error)
], debug=True)
