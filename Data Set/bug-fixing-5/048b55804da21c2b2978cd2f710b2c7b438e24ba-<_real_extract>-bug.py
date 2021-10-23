def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = mobj.group('id')
    display_id = mobj.group('display_id')
    webpage = self._download_webpage(url, display_id)
    video_url = self._html_search_regex("url: escape\\('([^']+)'\\)", webpage, 'url')
    title = self._html_search_regex('<h2 class="he2"><span>(.*?)</span>', webpage, 'title')
    thumbnail = self._html_search_regex('<span id="container"><img\\s+src="([^"]+)"', webpage, 'thumbnail', fatal=False)
    uploader = self._html_search_regex('class="aupa">\\s*(.*?)</a>', webpage, 'uploader')
    upload_date = unified_strdate(self._html_search_regex('Added: <strong>(.+?)</strong>', webpage, 'upload date', fatal=False))
    duration = parse_duration(self._search_regex('<td>Time:\\s*</td>\\s*<td align="right"><span>\\s*(.+?)\\s*</span>', webpage, 'duration', fatal=False))
    view_count = int_or_none(self._search_regex('<td>Views:\\s*</td>\\s*<td align="right"><span>\\s*(\\d+)\\s*</span>', webpage, 'view count', fatal=False))
    comment_count = int_or_none(self._search_regex('<td>Comments:\\s*</td>\\s*<td align="right"><span>\\s*(\\d+)\\s*</span>', webpage, 'comment count', fatal=False))
    categories = re.findall('<a href="[^"]+/search/video/desi"><span>([^<]+)</span></a>', webpage)
    return {
        'id': video_id,
        'display_id': display_id,
        'url': video_url,
        'http_headers': {
            'Referer': url,
        },
        'title': title,
        'thumbnail': thumbnail,
        'uploader': uploader,
        'upload_date': upload_date,
        'duration': duration,
        'view_count': view_count,
        'comment_count': comment_count,
        'categories': categories,
        'age_limit': 18,
    }