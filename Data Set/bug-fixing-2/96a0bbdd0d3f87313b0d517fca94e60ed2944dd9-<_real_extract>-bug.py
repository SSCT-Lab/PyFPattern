

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    player_data = self._parse_json(self._search_regex('videoLa7\\(({[^;]+})\\);', webpage, 'player data'), video_id, transform_source=js_to_json)
    return {
        '_type': 'url_transparent',
        'url': smuggle_url(('kaltura:103:%s' % player_data['vid']), {
            'service_url': 'http://kdam.iltrovatore.it',
        }),
        'id': video_id,
        'title': player_data['title'],
        'description': self._og_search_description(webpage, default=None),
        'thumbnail': player_data.get('poster'),
        'ie_key': 'Kaltura',
    }
