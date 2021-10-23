def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('http://docs.google.com/file/d/%s' % video_id), video_id)
    reason = self._search_regex('"reason"\\s*,\\s*"([^"]+)', webpage, 'reason', default=None)
    if reason:
        raise ExtractorError(reason)
    title = self._search_regex('"title"\\s*,\\s*"([^"]+)', webpage, 'title')
    duration = int_or_none(self._search_regex('"length_seconds"\\s*,\\s*"([^"]+)', webpage, 'length seconds', default=None))
    fmt_stream_map = self._search_regex('"fmt_stream_map"\\s*,\\s*"([^"]+)', webpage, 'fmt stream map').split(',')
    fmt_list = self._search_regex('"fmt_list"\\s*,\\s*"([^"]+)', webpage, 'fmt_list').split(',')
    resolutions = {
        
    }
    for fmt in fmt_list:
        mobj = re.search('^(?P<format_id>\\d+)/(?P<width>\\d+)[xX](?P<height>\\d+)', fmt)
        if mobj:
            resolutions[mobj.group('format_id')] = (int(mobj.group('width')), int(mobj.group('height')))
    formats = []
    for fmt_stream in fmt_stream_map:
        fmt_stream_split = fmt_stream.split('|')
        if (len(fmt_stream_split) < 2):
            continue
        (format_id, format_url) = fmt_stream_split[:2]
        f = {
            'url': lowercase_escape(format_url),
            'format_id': format_id,
            'ext': self._FORMATS_EXT[format_id],
        }
        resolution = resolutions.get(format_id)
        if resolution:
            f.update({
                'width': resolution[0],
                'height': resolution[1],
            })
        formats.append(f)
    self._sort_formats(formats)
    hl = self._search_regex('"hl"\\s*,\\s*"([^"]+)', webpage, 'hl', default=None)
    video_subtitles_id = None
    ttsurl = self._search_regex('"ttsurl"\\s*,\\s*"([^"]+)', webpage, 'ttsurl', default=None)
    if ttsurl:
        video_subtitles_id = ttsurl.encode('utf-8').decode('unicode_escape').split('=')[(- 1)]
    return {
        'id': video_id,
        'title': title,
        'thumbnail': self._og_search_thumbnail(webpage, default=None),
        'duration': duration,
        'formats': formats,
        'subtitles': self.extract_subtitles(video_id, video_subtitles_id, hl),
        'automatic_captions': self.extract_automatic_captions(video_id, video_subtitles_id, hl),
    }