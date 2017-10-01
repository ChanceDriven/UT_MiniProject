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


class LoginScreen(webapp2.RequestHandler):
    def get(self):
        # self.response.write(dir(ndb))
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/login.html')
        self.response.write(template.render())


class StreamRest(webapp2.RequestHandler):
    def get(self):
        # all streams
        all_streams = ndb.GqlQuery("select * from streams")
        self.response.write(all_streams)

    def get(self, stream_id):
        stream = ndb.GqlQuery("select * from streams "
                              "where id = :1", stream_id)
        self.response.write(stream)


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
    def get(self):
        user_id = ""
        subscribed_streams, authored_streams = services.get_manage_streams(user_id)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/manage.html')
        self.response.write(template.render(subscribed_streams=subscribed_streams, authored_streams=authored_streams))


class CreateStream(webapp2.RequestHandler):
    # Handler to create the stream information should be passed to the service to create
    # the object and store it.
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/create_stream.html')
        services.Service.create_stream("test", 5, "test2")
        self.response.write(template)

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/?', LoginScreen),
    (r'/login/(\w+)', Login),  # I need to remove this one and just put in the post
    (r'/manage/?', Management),
    (r'/streams', StreamRest),
    (r'/streams/(\w+)', StreamRest),
    (r'/create-stream', CreateStream),
    (r'/streams/trending', StreamTrending),
    (r'/streams/search/(\w+)', StreamSearch)
], debug=True)
