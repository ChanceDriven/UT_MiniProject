from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users
from google.cloud import datastore

import Models



def __init__(self):
        self

def create_stream(self, name,author,subscribers,image_url):
    '''This function creates the stream from the strings passed to the handler'''

    #name, author, subscribers, image_url)
    new_stream = Models.Stream(name,author,subscribers,image_url)
    datastore_client = datastore.Client()
    datastore_client.put()
    return 200





