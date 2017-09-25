from Models import models


class Service:
    def __init__(self):
        # type: () -> None
        pass

    @staticmethod
    def create_stream(name, subscribers, image_url):
        """
        :param name:
        :param subscribers:
        :param image_url:
        :return html:
        """

        # name, author, subscribers, image_url)
        new_stream = models.Stream()
        new_stream.name = name
        new_stream.subscribers = subscribers
        new_stream.imgUrl = image_url
        new_stream.put()
        return 200
