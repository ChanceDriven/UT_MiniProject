import os

import cgi
import jinja2
import webapp2
import logging
from services import services


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class HelloWebapp2(webapp2.RequestHandler):
    def get(self):
        self.redirect('/login')


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
    min_report_settings = 0

    def get(self):
        # change out with trending streams
        trending_streams = []
        trending_streams = services.get_trending_streams()

        min_report_settings = services.get_email_frequency()
        logging.info(min_report_settings)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/trending.html')
        self.response.write(template.render(trending_streams=trending_streams, report_settings = min_report_settings))

    def post(self):
        reportSettings = self.request.get_all('reporting')

        min_report_Settings = services.update_email_frequency(reportSettings)
        trending_streams = services.get_trending_streams()

        self.redirect('/streams/trending')


class StreamSearch(webapp2.RequestHandler):
    def get(self, query):
        streams = services.search_stream(query)
        self.response.write(streams)


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
        self.response.write(template.render())

    def post(self):
        subscribers = cgi.escape(self.request.get('subscribers')).split(',')
        stream_name = cgi.escape(self.request.get('streamname'))
        sub_message = cgi.escape(self.request.get('subscribers'))
        tags = cgi.escape(self.request.get('subscribers')).split(',')
        image_url = cgi.escape(self.request.get('imageurl'))
        services.create_stream(stream_name, subscribers, image_url, tags, sub_message)
        self.redirect('/manage')


class CalculateTrends(webapp2.RequestHandler):
    def get(self):
        result = services.calculate_trends()
        self.response.write(200)

class SendMail(webapp2.RequestHandler):
    def get(self):
        trending_streams = services.get_trending_streams()




class Error(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/error.html').render()
        self.response.write(template)

class Image(webapp2.RequestHandler):
    def post(self):
        stream_key = 'test'
        image = self.request.get('img')
        comments = self.request.get('comments')
        services.create_image(stream_key, comments, image)
        self.redirect('/streams/' + stream_key)



app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/?', LoginScreen),
    (r'/login/(\w+)', Login),  # I need to remove this one and just put in the post
    (r'/manage/?', Management),
    (r'/streams', AllStreams),
    (r'/streams/create/?', CreateStream),
    (r'/streams/trending/?', StreamTrending),
    (r'/streams/search/(\w+)', StreamSearch),
    (r'/streams/(\w+)', StreamRest),
    (r'/images', Image),
    (r'/calctrends', CalculateTrends),
    (r'/error', Error)
], debug=True)
