def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    video_url = urljoin(url, self._parse_json(self._search_regex('data-vnfo=(["\\\'])(?P<data>{.+?})\\1', webpage, 'data info', group='data'), video_id)[video_id])
    title = (self._search_regex('<[^>]+\\bclass=["\\\']PostEditTA[^>]+>([^<]+)', webpage, 'title', default=None) or self._og_search_description(webpage)).strip()
    thumbnail = self._og_search_thumbnail(webpage)
    return {
        'id': video_id,
        'url': video_url,
        'title': title,
        'thumbnail': thumbnail,
    }