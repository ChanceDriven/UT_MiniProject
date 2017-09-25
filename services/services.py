from google.cloud import datastore

from models import Stream


class Service:
    def __init__(self):
        pass

    def create_stream(self, name, author, subscribers, image_url):
        """
        :param name:
        :param author:
        :param subscribers:
        :param image_url:
        :return html:
        """

        # name, author, subscribers, image_url)
        new_stream = Stream(name, author, subscribers, image_url)
        datastore_client = datastore.Client()
        datastore_client.put(new_stream)
        return 200
