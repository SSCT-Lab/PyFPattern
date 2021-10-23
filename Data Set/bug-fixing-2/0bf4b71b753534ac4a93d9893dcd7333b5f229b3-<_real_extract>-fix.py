

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    title = self._html_search_meta('name', webpage)
    timestamp = parse_iso8601(self._html_search_meta('uploadDate', webpage))
    thumbnail = self._html_search_meta('thumbnailUrl', webpage)
    uploader_id = self._html_search_regex('<a class="item-to-subscribe" href="[^"]+/channels/([^/"]+)" title="Go to [^"]+ page">', webpage, 'uploader id', fatal=False)
    uploader = self._html_search_regex('<a class="item-to-subscribe" href="[^"]+/channels/[^/"]+" title="Go to ([^"]+) page">', webpage, 'uploader', fatal=False)
    categories_html = self._search_regex('(?s)><i class="icon icon-tag"></i>\\s*Categories / Tags\\s*.*?<ul class="[^"]*?list[^"]*?">(.*?)</ul>', webpage, 'categories', fatal=False)
    categories = None
    if categories_html:
        categories = [c.strip() for c in re.findall('(?s)<li><a.*?>(.*?)</a>', categories_html)]
    view_count = str_to_int(self._search_regex('<meta[^>]+itemprop="interactionCount"[^>]+content="UserPlays:([0-9,]+)">', webpage, 'view count', fatal=False))
    like_count = str_to_int(self._search_regex('<meta[^>]+itemprop="interactionCount"[^>]+content="UserLikes:([0-9,]+)">', webpage, 'like count', fatal=False))
    duration = parse_duration(self._html_search_meta('duration', webpage))
    media_id = self._search_regex('<button[^>]+data-id=(["\\\'])(?P<id>\\d+)\\1[^>]+data-quality=', webpage, 'media id', default=None, group='id')
    sources = [quality for (_, quality) in re.findall('<button[^>]+data-quality=(["\\\'])(.+?)\\1', webpage)]
    if (not (media_id and sources)):
        player_js = self._download_webpage(self._search_regex('<script[^>]id=(["\\\'])playerembed\\1[^>]+src=(["\\\'])(?P<url>.+?)\\2', webpage, 'player JS', group='url'), video_id, 'Downloading player JS')
        params_js = self._search_regex('\\$\\.ajax\\(url,\\ opts\\);\\s*\\}\\s*\\}\\)\\(([0-9,\\[\\] ]+)\\)', player_js, 'initialization parameters')
        params = self._parse_json(('[%s]' % params_js), video_id)
        media_id = params[0]
        sources = [('%s' % p) for p in params[2]]
    token_url = 'https://tkn.kodicdn.com/{0}/desktop/{1}'.format(media_id, '+'.join(sources))
    headers = {
        b'Content-Type': b'application/x-www-form-urlencoded',
        b'Origin': b'https://www.4tube.com',
    }
    token_req = sanitized_Request(token_url, b'{}', headers)
    tokens = self._download_json(token_req, video_id)
    formats = [{
        'url': tokens[format]['token'],
        'format_id': (format + 'p'),
        'resolution': (format + 'p'),
        'quality': int(format),
    } for format in sources]
    self._sort_formats(formats)
    return {
        'id': video_id,
        'title': title,
        'formats': formats,
        'categories': categories,
        'thumbnail': thumbnail,
        'uploader': uploader,
        'uploader_id': uploader_id,
        'timestamp': timestamp,
        'like_count': like_count,
        'view_count': view_count,
        'duration': duration,
        'age_limit': 18,
    }
