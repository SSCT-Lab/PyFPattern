

def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = (mobj.group('id') or mobj.group('path'))
    webpage = self._download_webpage(url, video_id)
    video_url = self._search_regex(['<div[^>]+?class="flowplayer[^>]+?data-href="([^"]+)"', '<a[^>]+?href="([^"]+)"[^>]+?class="videoplayer"'], webpage, 'video url')
    title = (self._og_search_title(webpage, default=None) or self._search_regex('<title>([^<]+)</title>', webpage, 'title'))
    duration = int_or_none(self._og_search_property('video:duration', webpage, 'duration', default=None))
    return {
        'id': video_id,
        'url': video_url,
        'title': title,
        'description': self._og_search_description(webpage, default=None),
        'thumbnail': self._og_search_thumbnail(webpage, default=None),
        'duration': duration,
    }
