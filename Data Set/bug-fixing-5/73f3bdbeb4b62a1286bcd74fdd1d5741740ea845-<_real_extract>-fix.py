def _real_extract(self, url):
    display_id = self._match_id(url)
    webpage = self._download_webpage(url, display_id)
    DATA_RE = 'data-%s=(["\\\'])(?P<value>(?:(?!\\1).)+)\\1'
    title = (self._search_regex((DATA_RE % 'video-title'), webpage, 'title', default=None, group='value') or self._og_search_title(webpage))
    video_id = self._search_regex((DATA_RE % 'job-id'), webpage, 'video id', group='value')
    video_path = self._search_regex((DATA_RE % 'video-path'), webpage, 'video path', group='value')
    video_available_abroad = self._search_regex((DATA_RE % 'video-available_abroad'), webpage, 'video available aboard', default='1', group='value')
    video_available_abroad = (video_available_abroad == '1')
    video_base = ('https://video%s.internazionale.it/%s/%s.' % (('' if video_available_abroad else '-ita'), video_path, video_id))
    formats = self._extract_m3u8_formats((video_base + 'm3u8'), display_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls', fatal=False)
    formats.extend(self._extract_mpd_formats((video_base + 'mpd'), display_id, mpd_id='dash', fatal=False))
    self._sort_formats(formats)
    timestamp = unified_timestamp(self._html_search_meta('article:published_time', webpage, 'timestamp'))
    return {
        'id': video_id,
        'display_id': display_id,
        'title': title,
        'thumbnail': self._og_search_thumbnail(webpage),
        'description': self._og_search_description(webpage),
        'timestamp': timestamp,
        'formats': formats,
    }