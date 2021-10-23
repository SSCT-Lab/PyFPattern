def fetch_list(self, params, link, query):
    '\n            :param params: a dict containing all of the fields relevant to build URL\n            :param link: a formatted URL\n            :param query: a formatted query string\n            :return the JSON response containing a list of instances.\n        '
    response = self.auth_session.get(link, params={
        'filter': query,
    })
    return self._return_if_object(self.fake_module, response)