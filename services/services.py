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

    # duplicate stream names are not allowed -- need to send back an error if this happens.
    new_stream = models.Stream()
    new_stream.name = name
    new_stream.subscribers = subscribers
    new_stream.imgUrl = image_url
    new_stream.put()
    return 200


def get_all_streams():
    """

    :return: a list of all the streams' names and the cover image URL  in the datastore sorted by createDate ascending
    """

    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()

    list_streams = [(stream.name, stream.coverImgUrl) for stream in all_streams]

    return json.dumps(list_streams)


def get_stream(stream_name = None, page_range = None ):
    """

    :param stream_name: the name of the stream
    :param page_range: the page range that you wish to fetch
    :return: returns the list of images and
    """
    if stream_name is None or stream_name is "":
        #place holder for now
        return "Fail: No Name Provide or stream name is empty"

    if page_range is None or page_range is "":
        #place holder for now
        return "Fail: No Page info provided or page_range is empty"

    stream_cls = models.Stream
    query = stream_cls.query(stream_cls.name == stream_name).order(-stream_cls.createdDate)
    stream = query.get()
    if stream is None:
        return "Fail: No Stream matches name provided"
    return json.dumps(stream)