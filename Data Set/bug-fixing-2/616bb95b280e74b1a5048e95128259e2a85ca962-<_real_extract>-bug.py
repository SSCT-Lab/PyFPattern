

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    info_url = self._html_search_regex('Misc\\.videoFLV\\(\\s*{\\s*data\\s*:\\s*"([^"]+)"', webpage, 'info url')
    parsed_url = compat_urlparse.urlparse(info_url)
    qs = compat_urlparse.parse_qs(parsed_url.query)
    qs.update({
        'reklama': ['0'],
        'type': ['js'],
    })
    info_url = compat_urlparse.urlunparse(parsed_url._replace(query=compat_urllib_parse_urlencode(qs, True)))
    json_info = self._download_json(info_url, video_id, transform_source=(lambda s: s[s.index('{'):(s.rindex('}') + 1)]))
    item = None
    for i in json_info['items']:
        if ((i.get('type') == 'video') or (i.get('type') == 'stream')):
            item = i
            break
    if (not item):
        raise ExtractorError('No suitable stream found')
    quality = qualities(('low', 'middle', 'high'))
    formats = []
    for fmt in item['video']:
        video_url = fmt.get('file')
        if (not video_url):
            continue
        format_ = fmt['format']
        format_id = ('%s_%s' % (format_, fmt['quality']))
        preference = None
        if (format_ in ('mp4', 'webm')):
            ext = format_
        elif (format_ == 'rtmp'):
            ext = 'flv'
        elif (format_ == 'apple'):
            ext = 'mp4'
            preference = (- 1)
        elif (format_ == 'adobe'):
            continue
        else:
            continue
        formats.append({
            'url': video_url,
            'ext': ext,
            'format_id': format_id,
            'quality': quality(fmt.get('quality')),
            'preference': preference,
        })
    self._sort_formats(formats)
    title = item['title']
    is_live = (item['type'] == 'stream')
    if is_live:
        title = self._live_title(title)
    description = (self._og_search_description(webpage, default=None) or self._html_search_meta('description', webpage, 'description'))
    timestamp = None
    duration = None
    if (not is_live):
        duration = int_or_none(item.get('length'))
        timestamp = item.get('published')
        if timestamp:
            timestamp = parse_iso8601(timestamp[:(- 5)])
    return {
        'id': video_id,
        'title': title,
        'description': description,
        'thumbnail': item.get('image'),
        'duration': duration,
        'timestamp': timestamp,
        'is_live': is_live,
        'formats': formats,
    }
