def _get_releases(self, query):
    'Returns a list of AlbumInfo objects for a beatport search query.\n        '
    query = re.sub('\\W+', ' ', query, re.UNICODE)
    query = re.sub('\\b(CD|disc)\\s*\\d+', '', query, re.I)
    albums = [self._get_album_info(x) for x in self.client.search(query).results]
    return albums