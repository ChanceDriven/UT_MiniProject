import os
import logging
import json

from google.appengine.api import images
import cgi
import jinja2
import webapp2
import logging
import urllib
import re
import json
from Models import models
from services import services

WEBSITE = 'https://blueimp.github.io/jQuery-File-Upload/'
MIN_FILE_SIZE = 1  # bytes
# Max file size is memcache limit (1MB) minus key size minus overhead:
MAX_FILE_SIZE = 999000  # bytes
IMAGE_TYPES = re.compile('image/(gif|p?jpeg|(x-)?png)')
ACCEPT_FILE_TYPES = IMAGE_TYPES
THUMB_MAX_WIDTH = 80
THUMB_MAX_HEIGHT = 80
THUMB_SUFFIX = '.' + str(THUMB_MAX_WIDTH) + 'x' + str(THUMB_MAX_HEIGHT) + '.png'
EXPIRATION_TIME = 300  # seconds
# If set to None, only allow redirects to the referer protocol+host.
# Set to a regexp for custom pattern matching against the redirect value:
REDIRECT_ALLOW_TARGET = None

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


# Note: My idea was to create new handlers that would return JSON
# instead of trying to setup another file and stripping things out.
class ApiStreamRest(webapp2.RequestHandler):
    
    def get(self):
        all_streams = services.get_all_streams()
        streams_json = []
        for stream in all_streams:
            streams_json.append(json.dumps(stream, cls=models.CustomEncoder))

        logging.info(json.dumps(streams_json))


class StreamTrending(webapp2.RequestHandler):
    min_report_settings = 0

    def get(self):
        # change out with trending streams
        trending_streams = services.get_trending_streams()

        min_report_settings = services.get_email_config()
        logging.info(min_report_settings)
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/trending.html')
        self.response.write(template.render(trending_streams=trending_streams, report_settings=min_report_settings))

    def post(self):
        reportSettings = self.request.get_all('reporting')

        min_report_Settings = services.update_email_frequency(reportSettings)
        trending_streams = services.get_trending_streams()

        self.redirect('/streams/trending')


class ApiStreamTrending(webapp2.RequestHandler):
    min_report_settings = 0

    def get(self):
        # change out with trending streams
        trending_streams_json = []
        trending_streams = services.get_trending_streams()

        min_report_settings = services.get_email_config()
        logging.info(min_report_settings)
        for stream in trending_streams:
            trending_streams_json.append(json.dumps(stream, cls=models.CustomEncoder))
            logging.info(json.dumps(stream))

        ret_trend_settings = {'trending_streams': trending_streams, "min_report_settings": min_report_settings}
        logging.info(ret_trend_settings)
        streams_json = json.dumps(ret_trend_settings, indent=4, cls=models.CustomEncoder)
        logging.info(streams_json)
        self.response.write(json.dumps(streams_json))

    def post(self):
        reportSettings = self.request.get_all('reporting')

        min_report_Settings = services.update_email_frequency(reportSettings)
        trending_streams = services.get_trending_streams()

        self.redirect('/streams/trending')


class StreamSearchSuggestions(webapp2.RequestHandler):
    def get(self):
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
        self.response.write({
            'subscribed_streams': subscribed_streams,
            'authored_streams': authored_streams
        })


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

        key = services.create_stream(stream_name, subscribers, image_url, tags, sub_message)
        self.response.write(key)


class CalculateTrends(webapp2.RequestHandler):
    def get(self):
        services.calculate_trends()
        self.response.write()


class SendMail(webapp2.RequestHandler):
    def get(self):

        emails = "ebsaibes@gmail.com,robbymrodriguez@gmail.com,ee382vta@gmail.com"

        trending_streams = services.get_trending_streams()
        email_config = services.get_email_config()

        if email_config is None:
            # don't send mail if nothing is returned
            pass
        else:
            services.send_mail(emails)
        self.response.write()


class Error(webapp2.RequestHandler):
    def get(self):
        # TODO: Not sure what to do with this
        template = JINJA_ENVIRONMENT.get_or_select_template('./views/error.html').render()
        self.response.write(template)


class Rebuild(webapp2.RequestHandler):
    def get(self):
        logging.info("rebuilding index started")
        services.delete_index()
        services.rebuild_search_index()
        self.response.write()


class CORSHandler(webapp2.RequestHandler):
    def cors(self):
        headers = self.response.headers
        headers['Access-Control-Allow-Origin'] = '*'
        headers['Access-Control-Allow-Methods'] = \
            'OPTIONS, HEAD, GET, POST, DELETE'
        headers['Access-Control-Allow-Headers'] = \
            'Content-Type, Content-Range, Content-Disposition'

    def initialize(self, request, response):
        super(CORSHandler, self).initialize(request, response)
        self.cors()

    def json_stringify(self, obj):
        return json.dumps(obj, separators=(',', ':'))

    def options(self, *args, **kwargs):
        pass


class UploadHandler(CORSHandler):
    def validate(self, file_stream):
        if file_stream['size'] < MIN_FILE_SIZE:
            logging.info("SKIPPING FOR FILE TOO SMALL")
            file_stream['error'] = 'File is too small'
        elif file_stream['size'] > MAX_FILE_SIZE:
            logging.info("SKIPPING FOR FILE TOO BIG")
            file_stream['error'] = 'File is too big'
        elif not ACCEPT_FILE_TYPES.match(file_stream['type']):
            logging.info("SKIPPING FOR FILE TYPE")
            file_stream['error'] = 'File type not allowed'
        else:
            return True
        return False

    def validate_redirect(self, redirect):
        if redirect:
            if REDIRECT_ALLOW_TARGET:
                return REDIRECT_ALLOW_TARGET.match(redirect)
            referer = self.request.headers['referer']
            if referer:
                from urlparse import urlparse
                parts = urlparse(referer)
                redirect_allow_target = '^' + re.escape(
                    parts.scheme + '://' + parts.netloc + '/'
                )
            return re.match(redirect_allow_target, redirect)
        return False

    @staticmethod
    def get_file_size(file_stream):
        file_stream.seek(0, 2)  # Seek to the end of the file
        size = file_stream.tell()  # Get the position of EOF
        file_stream.seek(0)  # Reset the file position to the beginning
        return size

    def handle_upload(self, stream_key):
        items = self.request.POST.items()
        logging.info(items)
        logging.info(str(len(items)))
        for name, fieldStorage in items:
            if type(fieldStorage) is unicode:
                logging.info("UNICODE")
                continue
            result = {
                'name': urllib.unquote(fieldStorage.filename),
                'type': fieldStorage.type,
                'size': self.get_file_size(fieldStorage.file)
            }
            logging.info("before validate")
            if self.validate(result):
                logging.info("after validate")
                services.create_image(stream_key, fieldStorage.file)
                logging.info("after save")

        self.redirect('/streams/' + stream_key)

    def head(self):
        pass

    def get(self, resource):
        logging.info(resource)
        image = services.get_any_entity(resource)
        self.response.headers[b'Content-Type'] = 'image/jpeg'
        self.response.write(image.content)

    def post(self, stream_key):
        logging.info("HEY I HIT THE POST")

        if self.request.get('_method') == 'DELETE':
            return self.delete()

        result = {'files': self.handle_upload(stream_key)}
        s = self.json_stringify(result)
        redirect = self.request.get('redirect')
        if self.validate_redirect(redirect):
            return self.redirect(str(
                redirect.replace('%s', urllib.quote(s, ''), 1)
            ))
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write(s)


class FileHandler(CORSHandler):
    @staticmethod
    def normalize(strng):
        return urllib.quote(urllib.unquote(strng), '')

    def get(self, resource):
        logging.info(resource)
        image = services.get_any_entity(resource)
        self.response.headers[b'Content-Type'] = 'image/jpeg'
        self.response.write(image.content)

    def delete(self, content_type, data_hash, file_name):
        content_type = self.normalize(content_type)
        file_name = self.normalize(file_name)
        key = content_type + '/' + data_hash + '/' + file_name
        content_type = urllib.unquote(content_type)
        if IMAGE_TYPES.match(content_type):
            thumbnail_key = key + THUMB_SUFFIX
        if 'application/json' in self.request.headers.get('Accept'):
            self.response.headers['Content-Type'] = 'application/json'
        self.response.write()


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
    (r'/images/(\w+\-?\w*)', UploadHandler),
    (r'/sendmail', SendMail),
    (r'/error', Error),
    (r'/rebuildIndex', Rebuild),
    # (r'/api/streams/create/?',ApiCreateStream),
    (r'/api/streams/trending/?', ApiStreamTrending),
    (r'/api/streams', ApiStreamRest)
], debug=True)
