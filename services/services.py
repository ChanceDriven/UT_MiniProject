from Models import models
import json


def create_stream(name, subscribers, image_url):
    """

    :return:
    :param name:
    :param subscribers:
    :param image_url:
    :return html:
    """

    new_stream = models.Stream()
    new_stream.name = name.upper()
    new_stream.subscribers = subscribers
    new_stream.imgUrl = image_url
    new_stream.put()
    return 200


def get_all_streams():
    """
    :return (list):
    """
    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()
    return all_streams


def search_streams(text):
    """
    :param text:
    :return:
    """
    # this will only work if the names are always upper
    # or else we can do something like pull all of them into memory
    text = text.upper()
    limit = text[:-1] + chr(ord(text[-1]) + 1)
    temp_stream = models.Stream
    return temp_stream \
        .query(temp_stream.name >= text, temp_stream.name < limit) \
        .order(temp_stream.createdDate) \
        .fetch()
