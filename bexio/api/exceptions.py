class BexioError(Exception):
    pass


class BexioAPIError(BexioError):

    def __init__(self, message, url, status_code):
        self.url = url
        self.status_code = status_code
        super().__init__(message)
