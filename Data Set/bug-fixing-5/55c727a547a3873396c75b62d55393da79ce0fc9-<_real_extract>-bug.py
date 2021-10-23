def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    title = remove_end(self._og_search_title(webpage), ' - NDTV')
    filename = self._search_regex("__filename='([^']+)'", webpage, 'video filename')
    video_url = ('http://bitcast-b.bitgravity.com/ndtvod/23372/ndtv/%s' % filename)
    duration = int_or_none(self._search_regex("__duration='([^']+)'", webpage, 'duration', fatal=False))
    upload_date = unified_strdate(self._html_search_meta('publish-date', webpage, 'upload date', fatal=False))
    description = remove_end(self._og_search_description(webpage), ' (Read more)')
    return {
        'id': video_id,
        'url': video_url,
        'title': title,
        'description': description,
        'thumbnail': self._og_search_thumbnail(webpage),
        'duration': duration,
        'upload_date': upload_date,
    }