import os
import json
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


class AllStreams(webapp2.RequestHandler):
    def get(self):
        # all streams
        all_streams = services.get_all_streams()
        template = JINJA_ENVIRONMENT.get_or_select_template('/views/all_streams.html')
        self.response.write(template.render(streams=all_streams))


class StreamRest(webapp2.RequestHandler):
    def get(self):
        # all streams
        all_streams = services.get_all_streams()
        template = JINJA_ENVIRONMENT.get_or_select_template('/views/all_streams.html')
        self.response.write(template.render(streams=all_streams))


    def get(self, stream_id):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/stream.html')
        stream = services.get_stream(stream_id)
        self.response.write(template.render(stream=stream, index=0, length=len(stream.images)))


class StreamTrending(webapp2.RequestHandler):
    def get(self):
        # change out with trending streams

        self.response.write(all_streams)


class StreamSearch(webapp2.RequestHandler):
    def get(self):
        # change out with trending streams
        json_results = []
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/search.html')
        self.response.write(template.render(results = json_results))

    def post(self, search):
        raw_results = services.search_stream(search)
        json_results = json.loads(raw_results)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/search.html')
        self.response.write(template.render(results = json_results))


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

class Error(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/error.html').render()
        self.response.write(template)


app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/?', LoginScreen),
    (r'/login/(\w+)', Login),  # I need to remove this one and just put in the post
    (r'/manage/?', Management),
    (r'/streams', AllStreams),
    (r'/streams/(\w+)', StreamRest),
    (r'/create-stream', CreateStream),
    (r'/streams/trending', StreamTrending),
    (r'/streams/search/(\w+)', StreamSearch),
    (r'/search',StreamSearch),
    (r'/error', Error)
], debug=True)
