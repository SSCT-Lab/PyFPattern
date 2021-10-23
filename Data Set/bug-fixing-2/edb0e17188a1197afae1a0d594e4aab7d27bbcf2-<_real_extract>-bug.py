

def _real_extract(self, url):
    video_id = self._match_id(url)
    (webpage, urlh) = self._download_webpage_handle(url, video_id)
    hostname = compat_urllib_parse_urlparse(urlh.geturl()).hostname
    age_limit = (18 if (hostname.split('.')[0] == 'ecchi') else 0)
    video_data = self._download_json(('http://www.iwara.tv/api/video/%s' % video_id), video_id)
    if (not video_data):
        iframe_url = self._html_search_regex('<iframe[^>]+src=([\\\'"])(?P<url>[^\\\'"]+)\\1', webpage, 'iframe URL', group='url')
        return {
            '_type': 'url_transparent',
            'url': iframe_url,
            'age_limit': age_limit,
        }
    title = remove_end(self._html_search_regex('<title>([^<]+)</title>', webpage, 'title'), ' | Iwara')
    formats = []
    for a_format in video_data:
        format_id = a_format.get('resolution')
        height = int_or_none(self._search_regex('(\\d+)p', format_id, 'height', default=None))
        formats.append({
            'url': a_format['uri'],
            'format_id': format_id,
            'ext': (mimetype2ext(a_format.get('mime')) or 'mp4'),
            'height': height,
            'width': int_or_none((((height / 9.0) * 16.0) if height else None)),
            'quality': (1 if (format_id == 'Source') else 0),
        })
    self._sort_formats(formats)
    return {
        'id': video_id,
        'title': title,
        'age_limit': age_limit,
        'formats': formats,
    }
