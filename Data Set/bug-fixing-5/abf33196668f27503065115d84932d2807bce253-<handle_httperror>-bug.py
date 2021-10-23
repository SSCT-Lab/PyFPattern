def handle_httperror(self, exc):
    'Overridable method for dealing with HTTP codes.\n\n        This method will attempt to handle known cases of HTTP status codes.\n        If your API uses status codes to convey information in a regular way,\n        you can override this method to handle it appropriately.\n\n        :returns:\n            * True if the code has been handled in a way that the request\n            may be resent without changes.\n            * False if the error cannot be handled or recovered from by the\n            plugin. This will result in the HTTPError being returned to the\n            caller to deal with as appropriate.\n            * Any other value returned is taken as a valid response from the\n            server without making another request. In many cases, this can just\n            be the original exception.\n            '
    if ((exc.code == 401) and self.connection._auth):
        self.connection._auth = None
        self.login(self.connection.get_option('remote_user'), self.connection.get_option('password'))
        return True
    return exc