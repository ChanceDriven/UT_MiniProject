from google.appengine.ext import db
from google.appengine.api import users


class Service:
    def create_stream(self, stream):
        '''This function creates the stream from the strings passed to the handler'''
        new_stream = Stream('','','','')
