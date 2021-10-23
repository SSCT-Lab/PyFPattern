def _real_extract(self, url):
    display_id = self._match_id(url)
    webpage = self._download_webpage(url, display_id)
    brightcove_id = self._search_regex(['<[^>]+\\bid=["\\\']bc_(\\d+)', "getVideo\\('[^']+video_id=(\\d+)"], webpage, 'brightcove id')
    return self.url_result((self.BRIGHTCOVE_URL_TEMPLATE % brightcove_id), 'BrightcoveNew', brightcove_id)