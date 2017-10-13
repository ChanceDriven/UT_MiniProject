import os
import logging
import json

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

        min_report_settings = services.get_email_config()
        logging.info(min_report_settings)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/trending.html')
        self.response.write(template.render(trending_streams=trending_streams, report_settings = min_report_settings))

    def post(self):
        reportSettings = self.request.get_all('reporting')

        min_report_Settings = services.update_email_frequency(reportSettings)
        trending_streams = services.get_trending_streams()

        self.redirect('/streams/trending')


class StreamSearchSuggestions(webapp2.RequestHandler):
    def get(self, query=""):
        term = self.request.get('term')     
        suggestions = services.get_search_suggestions(term)
        self.response.write(json.dumps(suggestions))


class StreamSearch(webapp2.RequestHandler):
    def get(self, query=""):
        streams = services.search_stream(query)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/search.html')
        self.response.write(template.render(results=streams, count=len(streams)))


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

        matching_stream = services.get_stream_by_name(stream_name)
        logging.info(matching_stream)
        if matching_stream is not None:
            self.redirect('/error')
            return

        services.create_stream(stream_name, subscribers, image_url, tags, sub_message)
        self.redirect('/manage')


class CalculateTrends(webapp2.RequestHandler):
    def get(self):
        result = services.calculate_trends()
        self.response.write(200)


class SendMail(webapp2.RequestHandler):
    def get(self):

        emails = "ebsaibes@gmail.com,robbymrodriguez@gmail.com,ee382vta@gmail.com"

        trending_streams = services.get_trending_streams()
        email_config = services.get_email_config()


        if email_config is None:
            #don't send mail if nothing is returned
            return
        else:
            result = services.send_mail(emails)



class Error(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/error.html').render()
        self.response.write(template)


class Rebuild(webapp2.RequestHandler):
    def get(self):
        logging.info("rebuilding index started")
        services.delete_index()
        services.rebuild_search_index()
        self.response.write(200)


class ImgServe(webapp2.RequestHandler):

    def get(self, resource):
        logging.info(resource)
        image = services.get_any_entity(resource)
        self.response.headers[b'Content-Type'] = 'image/jpeg'
        self.response.write(image.content)

    def post(self, stream_key):
        image = self.request.get('img')
        comments = self.request.get('comments')
        services.create_image(stream_key, comments, image)
        logging.info("STREAM KEY " + stream_key)
        self.redirect('/streams/' + stream_key)



app = webapp2.WSGIApplication([
    ('/', HelloWebapp2),
    (r'/login/?', LoginScreen),
    (r'/login/(\w+)', Login),  # I need to remove this one and just put in the post
    (r'/manage/?', Management),
    (r'/streams', AllStreams),
    (r'/streams/create/?', CreateStream),
    (r'/streams/trending/?', StreamTrending),
    (r'/streams/search/?', StreamSearch),
    (r'/streams/search/(\w)', StreamSearch),
    (r'/streams/search_suggestions', StreamSearchSuggestions),
    (r'/streams/(\w+\-?\w*)', StreamRest),
    (r'/calctrends', CalculateTrends),
    (r'/images/(\w+\-?\w*)', ImgServe),
    (r'/sendmail', SendMail),
    (r'/error', Error),
    (r'/rebuildIndex',Rebuild)
], debug=True)
