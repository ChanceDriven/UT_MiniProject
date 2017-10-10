import json
import datetime
import re
import logging
import os

from Models import models
from google.appengine.ext import ndb
from google.appengine.api import mail


def create_stream(name, subscribers=[], image_url="", tags=[], message_to_subs=""):
    """

    :return:
    :param name:
    :param subscribers:
    :param image_url:
    :param tags:
    :param message_to_subs:
    :return html:

    """

    # duplicate stream names are not allowed -- need to send back an error if this happens.
    new_stream = models.Stream()
    new_stream.name = name
    new_stream.subscribers = subscribers
    new_stream.imgUrl = image_url
    new_stream.tags = tags
    return new_stream.put()


def create_image(stream_id, comments, image):
    new_image = models.Image(comments, image)
    image_key = new_image.put()
    stream = ndb.Key(urlsafe=stream_id).get()
    stream.images = [] if stream.images is None else stream.images
    stream.images.append(image_key)
    stream.put()


def get_all_streams():
    """
    :return: a list of all the streams' names and the cover image URL  in the datastore sorted by createDate ascending
    """

    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.createdDate)
    all_streams = query.fetch()

    # list_streams = [{"name": stream.name, "coverImgUrl":stream.coverImgUrl} for stream in all_streams]

    return all_streams


def get_any_entity(urlsafe_key):
    return ndb.Key(urlsafe=urlsafe_key).get()


def get_stream(stream_id):
    """
    :param stream_id: the name of the stream
    :return: returns the stream
    """

    temp_stream = models.Stream
    # query = temp_stream.query(temp_stream.key == stream_id)
    query = temp_stream.query()
    stream = query.fetch()[0]
    add_stream_visits(stream.key)
    if stream is None:
        return "Fail: No Stream matches name provided"
    return stream


def get_trending_streams():
    temp_stream = models.Stream
    query = temp_stream.query().order(temp_stream.rank)
    trending_streams = query.fetch(3)
    return trending_streams


def add_stream_visits(key):
    """
    :param key: name of the stream that was visited
    :return: Return status code if update failed or succeeded
    """
    views = []
    temp_stream = models.Stream
    query = temp_stream.query(temp_stream.key == key)
    stream = query.get()
    if stream is None:
        return 400
    else:
        if stream.views is None:
            stream.views = views

        stream.views.append(datetime.datetime.now())
        logging.info(stream.views)
        logging.info(str(stream))
        stream.put()
        return 200


def calculate_trends():
    """

    :return:
    """
    flush = flush_views()
    rank = rank_streams()

    if flush < 300 and rank < 300:
        return 200
    else:
        return 400


def flush_views():
    """
    flushes the view count and resets the ranks to the stream
    :return:
    """
    temp_stream = models.Stream
    query = temp_stream.query()
    all_streams = query.fetch()
    if all_streams is None:
        return 400
    else:
        for stream in all_streams:
            if stream.view_count > 0:
                temp_views = [x for x in stream.views if x > (datetime.datetime.now() - datetime.timedelta(hours=1))]
                stream.views = temp_views
                stream.rank = 99
                stream.put()
        return 200


def rank_streams():
    temp_stream = models.Stream
    # order by the number of views desc
    query = temp_stream.query().order(-temp_stream.view_count).order(temp_stream.name)
    top_streams_list = query.fetch(3)
    if top_streams_list is None:
        return 400

    # iterate over list, the index will be set as the rank
    for index, stream in enumerate(top_streams_list):
        stream.rank = index
        stream.put()
    return 200



def get_search_suggestions(searchstring):
    logging.info("search string was: " + searchstring)
    streams = get_all_streams()
    suggestions_name = [x for x in streams if searchstring in x.name]
    logging.info(suggestions_name)
    return suggestions_name


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

    return find_list


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
    return all_streams, all_streams


def get_stream_by_name(name):
    temp_stream = models.Stream
    streams = temp_stream.query(temp_stream.name == name).fetch()
    logging.info("READ THIS")
    logging.info(name)
    logging.info(len(streams))
    if streams:
        return streams[0]
    return None


def update_email_frequency(reporting_values):
    """

    :param reporting_values: values of how often to send email digest
    :return: returns the minimum reporting frequency of all the values
    """
    email_config = models.EmailConfig
    min_report_freq = 0
    query = email_config.query()
    email_config = query.get()
    if email_config is None:
        email_config = models.EmailConfig()
        email_config.reportFrequency = min_report_freq


    else:
        min_report_freq = min(reporting_values)
        email_config.reportFrequency = int(min_report_freq)

    email_config.put()

    return min_report_freq


def get_email_config():
    """
    Gets the email frequency setting for the page
    :return: the minimum setting that was set by an admin.  If not set, it will return 0
    """
    query = models.EmailConfig.query()
    email_config = query.get()

    if email_config is None:
        return None

    return email_config


def send_mail(emails):

    email_config = get_email_config()
    trending_streams = get_trending_streams()

    if email_config is None:
        return
    else:
        body = "The top 3 trending streams are: " + os.linesep
        if len(trending_streams) < 0:
            body += "There are no trending streams"
        else:
            streams = ""
            for stream in trending_streams:
                body += stream.name + " | " + str(stream.view_count) + " " + os.linesep

        senders = "ebsaibes@gmail.com"
        subject = "Team Cobalt: Email Digest"
        to = emails
        mail.send_mail(senders, to, subject, body)
        email_config.lastEmailSent = datetime.datetime.now()
        email_config.put()



