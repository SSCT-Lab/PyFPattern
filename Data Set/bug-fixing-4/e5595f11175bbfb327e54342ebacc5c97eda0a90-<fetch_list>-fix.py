def fetch_list(self, params, link, query):
    '\n            :param params: a dict containing all of the fields relevant to build URL\n            :param link: a formatted URL\n            :param query: a formatted query string\n            :return the JSON response containing a list of instances.\n        '
    lists = []
    resp = self._return_if_object(self.fake_module, self.auth_session.get(link, params={
        'filter': query,
    }))
    lists.append(resp.get('items'))
    while resp.get('nextPageToken'):
        resp = self._return_if_object(self.fake_module, self.auth_session.get(link, params={
            'filter': query,
            'pageToken': resp.get('nextPageToken'),
        }))
        lists.append(resp.get('items'))
    return self.build_list(lists)