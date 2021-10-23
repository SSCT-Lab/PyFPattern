def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = mobj.group('id')
    display_id = mobj.group('display_id')
    webpage = self._download_webpage(url, display_id)
    info_dict = self._parse_html5_media_entries(url, webpage, video_id)[0]
    title = self._html_search_regex(('<title>(.+?)\\s*-\\s*Indian\\s+Porn</title>', '<h4>(.+?)</h4>'), webpage, 'title')
    duration = parse_duration(self._search_regex('Time:\\s*<strong>\\s*(.+?)\\s*</strong>', webpage, 'duration', fatal=False))
    view_count = int(self._search_regex('(?s)Time:\\s*<strong>.*?</strong>.*?<strong>\\s*(\\d+)\\s*</strong>', webpage, 'view count', fatal=False))
    categories = re.findall('<a[^>]+class=[\\\'"]categories[\\\'"][^>]*>\\s*([^<]+)\\s*</a>', webpage)
    info_dict.update({
        'id': video_id,
        'display_id': display_id,
        'http_headers': {
            'Referer': url,
        },
        'title': title,
        'duration': duration,
        'view_count': view_count,
        'categories': categories,
        'age_limit': 18,
    })
    return info_dict