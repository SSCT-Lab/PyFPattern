

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('https://chaturbate.com/%s/' % video_id), video_id, headers=self.geo_verification_headers())
    m3u8_urls = []
    for m in re.finditer('(["\\\'])(?P<url>http.+?\\.m3u8.*?)\\1', webpage):
        (m3u8_fast_url, m3u8_no_fast_url) = (m.group('url'), m.group('url').replace('_fast', ''))
        for m3u8_url in (m3u8_fast_url, m3u8_no_fast_url):
            if (m3u8_url not in m3u8_urls):
                m3u8_urls.append(m3u8_url)
    if (not m3u8_urls):
        error = self._search_regex(['<span[^>]+class=(["\\\'])desc_span\\1[^>]*>(?P<error>[^<]+)</span>', '<div[^>]+id=(["\\\'])defchat\\1[^>]*>\\s*<p><strong>(?P<error>[^<]+)<'], webpage, 'error', group='error', default=None)
        if (not error):
            if any(((p in webpage) for p in (self._ROOM_OFFLINE, 'offline_tipping', 'tip_offline'))):
                error = self._ROOM_OFFLINE
        if error:
            raise ExtractorError(error, expected=True)
        raise ExtractorError('Unable to find stream URL')
    formats = []
    for m3u8_url in m3u8_urls:
        m3u8_id = ('fast' if ('_fast' in m3u8_url) else 'slow')
        formats.extend(self._extract_m3u8_formats(m3u8_url, video_id, ext='mp4', preference=((- 10) if (m3u8_id == 'fast') else None), m3u8_id=m3u8_id, fatal=False, live=True))
    self._sort_formats(formats)
    return {
        'id': video_id,
        'title': self._live_title(video_id),
        'thumbnail': ('https://roomimg.stream.highwebmedia.com/ri/%s.jpg' % video_id),
        'age_limit': self._rta_search(webpage),
        'is_live': True,
        'formats': formats,
    }
