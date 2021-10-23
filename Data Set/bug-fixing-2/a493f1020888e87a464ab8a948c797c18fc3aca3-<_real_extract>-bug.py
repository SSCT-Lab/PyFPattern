

def _real_extract(self, url):
    video_id = self._match_id(url)
    request = sanitized_Request(url)
    request.add_header('User-Agent', self._USER_AGENT_IPAD)
    webpage = self._download_webpage(request, video_id)
    title = self._html_search_regex('<title>([^<]*)</title>', webpage, 'title')
    regex = '<div *class=[\'"]video_img[^>]*data-url=[\'"]([^\'"]*\\.jpg)[\'"]'
    thumbnail = self._html_search_regex(regex, webpage, '')
    regex = ('<video *[^>]*src=[\'"]([^\'"]*)[\'"]',)
    video_url = self._html_search_regex(regex, webpage, '')
    return {
        'id': video_id,
        'title': title,
        'url': video_url,
        'thumbnail': thumbnail,
    }
