def _real_extract(self, url):
    video_id = self._match_id(url)
    url_pattern = ('https://openload.co/%%s/%s/' % video_id)
    headers = {
        'User-Agent': self._USER_AGENT,
    }
    for path in ('embed', 'f'):
        page_url = (url_pattern % path)
        last = (path == 'f')
        webpage = self._download_webpage(page_url, video_id, ('Downloading %s webpage' % path), headers=headers, fatal=last)
        if (not webpage):
            continue
        if (('File not found' in webpage) or ('deleted by the owner' in webpage)):
            if (not last):
                continue
            raise ExtractorError('File not found', expected=True, video_id=video_id)
        break
    phantom = PhantomJSwrapper(self, required_version='2.0')
    (webpage, _) = phantom.get(page_url, html=webpage, video_id=video_id, headers=headers)
    decoded_id = (get_element_by_id('streamurl', webpage) or get_element_by_id('streamuri', webpage) or get_element_by_id('streamurj', webpage) or self._search_regex(('>\\s*([\\w-]+~\\d{10,}~\\d+\\.\\d+\\.0\\.0~[\\w-]+)\\s*<', '>\\s*([\\w~-]+~\\d+\\.\\d+\\.\\d+\\.\\d+~[\\w~-]+)'), webpage, 'stream URL'))
    video_url = ('https://openload.co/stream/%s?mime=true' % decoded_id)
    title = (self._og_search_title(webpage, default=None) or self._search_regex('<span[^>]+class=["\\\']title["\\\'][^>]*>([^<]+)', webpage, 'title', default=None) or self._html_search_meta('description', webpage, 'title', fatal=True))
    entries = self._parse_html5_media_entries(page_url, webpage, video_id)
    entry = (entries[0] if entries else {
        
    })
    subtitles = entry.get('subtitles')
    info_dict = {
        'id': video_id,
        'title': title,
        'thumbnail': (entry.get('thumbnail') or self._og_search_thumbnail(webpage, default=None)),
        'url': video_url,
        'ext': determine_ext(title, 'mp4'),
        'subtitles': subtitles,
        'http_headers': headers,
    }
    return info_dict