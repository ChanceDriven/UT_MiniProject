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

    list_streams = [{"name": stream.name, "coverImgUrl":stream.coverImgUrl} for stream in all_streams]

    return json.dumps(dict_streams)


def get_stream(stream_name=None, page_range=None):
    """

    :param stream_name: the name of the stream
    :param page_range: the page range that you wish to fetch
    :return: returns the list of images and
    """
    if stream_name is None or stream_name is "":
        # place holder for now
        return "Fail: No Name Provide or stream name is empty"

    if page_range is None or page_range is "":
        # place holder for now
        return "Fail: No Page info provided or page_range is empty"

    temp_image = models.Image
    query = temp_image.query(temp_image.streamName == stream_name).order(-temp_image.createdDate)
    images = query.fetch(page_range)
    if images is None:
        return "Fail: No Stream matches name provided"
    return json.dumps(images, len(images))


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
