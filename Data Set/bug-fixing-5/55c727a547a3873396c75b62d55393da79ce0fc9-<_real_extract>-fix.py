def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    title = compat_urllib_parse_unquote_plus((self._search_regex("__title\\s*=\\s*'([^']+)'", webpage, 'title', default=None) or self._og_search_title(webpage)))
    filename = self._search_regex("(?:__)?filename\\s*[:=]\\s*'([^']+)'", webpage, 'video filename')
    video_url = urljoin('https://ndtvod.bc-ssl.cdn.bitgravity.com/23372/ndtv/', filename.lstrip('/'))
    duration = parse_duration(self._search_regex("(?:__)?duration\\s*[:=]\\s*'([^']+)'", webpage, 'duration', fatal=False))
    upload_date = unified_strdate((self._html_search_meta('publish-date', webpage, 'upload date', default=None) or self._html_search_meta('uploadDate', webpage, 'upload date', default=None) or self._search_regex('datePublished"\\s*:\\s*"([^"]+)"', webpage, 'upload date', fatal=False)))
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