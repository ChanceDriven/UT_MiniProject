from Models import models
import json


@staticmethod
def create_stream(name, subscribers, image_url):
    """

    :return:
    :param name:
    :param subscribers:
    :param image_url:
    :return html:
    """

    new_stream = models.Stream()
    new_stream.name = name
    new_stream.subscribers = subscribers
    new_stream.imgUrl = image_url
    new_stream.put()
    return 200


def get_all_streams():
    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()
    return all_streams
