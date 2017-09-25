from Models import models


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
        new_stream = models.Stream(name, author, subscribers, image_url)
        new_stream.put()
        return 200
