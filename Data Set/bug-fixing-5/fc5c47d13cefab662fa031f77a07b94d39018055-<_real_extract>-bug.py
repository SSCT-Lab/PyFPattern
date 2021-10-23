def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('http://vodplayer.parliamentlive.tv/?mid=' + video_id), video_id)
    widget_config = self._parse_json(self._search_regex('kWidgetConfig\\s*=\\s*({.+});', webpage, 'kaltura widget config'), video_id)
    kaltura_url = ('kaltura:%s:%s' % (widget_config['wid'][1:], widget_config['entry_id']))
    event_title = self._download_json(('http://parliamentlive.tv/Event/GetShareVideo/' + video_id), video_id)['event']['title']
    return {
        '_type': 'url_transparent',
        'id': video_id,
        'title': event_title,
        'description': '',
        'url': kaltura_url,
        'ie_key': 'Kaltura',
    }