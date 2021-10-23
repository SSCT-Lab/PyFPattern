

def _real_extract(self, url):
    video_id = self._match_id(url)
    request = sanitized_Request(url)
    request.add_header('User-Agent', self._USER_AGENT_IPAD)
    webpage = self._download_webpage(request, video_id)
    title = self._html_search_regex('<title>([^<]*)</title>', webpage, 'title')
    regex = '<div *class=[\'"]video_img[^>]*data-url=[\'"]([^\'"]*\\.jpg)[\'"]'
    thumbnail = self._html_search_regex(regex, webpage, '')
    videos = self._parse_html5_media_entries(url, webpage, video_id)
    info = videos[0]
    info.update({
        'id': video_id,
        'title': title,
        'thumbnail': thumbnail,
    })
    return info
