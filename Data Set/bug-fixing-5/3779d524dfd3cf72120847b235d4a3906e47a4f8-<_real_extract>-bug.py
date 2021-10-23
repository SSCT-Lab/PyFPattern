def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    video_title = self._og_search_title(webpage).replace('LiveLeak.com -', '').strip()
    video_description = self._og_search_description(webpage)
    video_uploader = self._html_search_regex('By:.*?(\\w+)</a>', webpage, 'uploader', fatal=False)
    age_limit = int_or_none(self._search_regex('you confirm that you are ([0-9]+) years and over.', webpage, 'age limit', default=None))
    video_thumbnail = self._og_search_thumbnail(webpage)
    sources_raw = self._search_regex('(?s)sources:\\s*(\\[.*?\\]),', webpage, 'video URLs', default=None)
    if (sources_raw is None):
        alt_source = self._search_regex('(file: ".*?"),', webpage, 'video URL', default=None)
        if alt_source:
            sources_raw = ('[{ %s}]' % alt_source)
        else:
            embed_url = self._search_regex('<iframe[^>]+src="(http://www.prochan.com/embed\\?[^"]+)"', webpage, 'embed URL')
            return {
                '_type': 'url_transparent',
                'url': embed_url,
                'id': video_id,
                'title': video_title,
                'description': video_description,
                'uploader': video_uploader,
                'age_limit': age_limit,
            }
    sources_json = re.sub('\\s([a-z]+):\\s', '"\\1": ', sources_raw)
    sources = json.loads(sources_json)
    formats = [{
        'format_id': ('%s' % i),
        'format_note': s.get('label'),
        'url': s['file'],
    } for (i, s) in enumerate(sources)]
    for (i, s) in enumerate(sources):
        orig_url = re.sub('\\.h264_.+?\\.mp4', '', s['file'])
        if (s['file'] != orig_url):
            formats.append({
                'format_id': ('original-%s' % i),
                'format_note': s.get('label'),
                'url': orig_url,
                'preference': 1,
            })
    self._sort_formats(formats)
    return {
        'id': video_id,
        'title': video_title,
        'description': video_description,
        'uploader': video_uploader,
        'formats': formats,
        'age_limit': age_limit,
        'thumbnail': video_thumbnail,
    }