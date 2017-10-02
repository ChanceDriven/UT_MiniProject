import json
import re

from Models import models
from google.appengine.ext import ndb


def create_stream(name, subscribers, image_url):
    """

    :return:
    :param name:
    :param subscribers:
    :param image_url:
    :return html:

    """

    # duplicate stream names are not allowed -- need to send back an error if this happens.
    new_stream = models.Stream()
    new_stream.name = name
    new_stream.subscribers = subscribers
    new_stream.imgUrl = image_url
    new_stream.put()
    return 200


def create_image(stream_name, image_url):
    new_image = models.Image(parent=ndb.Key("Stream", stream_name or "None"))
    new_image.streamName = stream_name
    new_image.imgUrl = image_url
    key = new_image.put()
    return key


def get_all_streams():
    """
    :return: a list of all the streams' names and the cover image URL  in the datastore sorted by createDate ascending
    """

    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()

    #list_streams = [{"name": stream.name, "coverImgUrl":stream.coverImgUrl} for stream in all_streams]

    return all_streams


def get_stream(stream_id):
    """
    :param stream_id: the name of the stream
    :return: returns the stream
    """

    temp_stream = models.Stream
    # query = temp_stream.query(temp_stream.key == stream_id)
    query = temp_stream.query()
    stream = query.fetch()[0]
    stream.images = ["demo1", "demo2", "demo3", "demo4", "demo5"]
    if stream is None:
        return "Fail: No Stream matches name provided"
    return stream

def get_trending_streams():
    temp_stream = models.Stream
    query = temp_stream.query('Streams with the highest hit rates in last hour').order(temp_stream.views)
    trending_streams = query.fetch(3)
    return trending_streams




def search_stream(string):
    """
    :param string:
    :return (array):
    """

    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()

    find_list = []
    for stream in all_streams:
        if string.upper() in stream.name.upper():
            find_list.append(stream)
            if len(find_list) > 4:
                break
                # This limits the results to 5 at most

    return json.dumps(find_list)


def upload_image(stream_id, data, name):
    temp_stream = models.Stream
    stream = temp_stream.query(temp_stream.key == stream_id).fetch()
    if stream.imgUrls is None:
        stream.imgUrls = []

    new_image = models.Image(name, data)
    img_key = new_image.put()
    stream.imgUrls.append(img_key)


def get_manage_streams(user_id):
    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()

    my_streams = []
    subscribed_streams = []
    for stream in all_streams:
        if stream.author == user_id:
            my_streams.append(stream)
            subscribed_streams.append(stream)
    return my_streams, subscribed_streams
