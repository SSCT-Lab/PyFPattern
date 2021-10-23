def _extract_info(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = mobj.group('id')
    display_id = ((mobj.group('display_id') if ('display_id' in mobj.groupdict()) else None) or mobj.group('id'))
    webpage = self._download_webpage(url, display_id, headers={
        'Cookie': 'age_verified=1',
    })
    formats = []
    format_urls = set()
    title = None
    thumbnail = None
    duration = None
    encrypted = False

    def extract_format(format_url, height=None):
        if ((not isinstance(format_url, compat_str)) or (not format_url.startswith('http'))):
            return
        if (format_url in format_urls):
            return
        format_urls.add(format_url)
        tbr = int_or_none(self._search_regex('[/_](\\d+)[kK][/_]', format_url, 'tbr', default=None))
        if (not height):
            height = int_or_none(self._search_regex('[/_](\\d+)[pP][/_]', format_url, 'height', default=None))
        if encrypted:
            format_url = aes_decrypt_text(video_url, title, 32).decode('utf-8')
        formats.append({
            'url': format_url,
            'format_id': (('%dp' % height) if height else None),
            'height': height,
            'tbr': tbr,
        })
    flashvars = self._parse_json(self._search_regex('flashvars\\s*=\\s*({.+?});', webpage, 'flashvars', default='{}'), display_id, fatal=False)
    if flashvars:
        title = flashvars.get('video_title')
        thumbnail = flashvars.get('image_url')
        duration = int_or_none(flashvars.get('video_duration'))
        encrypted = (flashvars.get('encrypted') is True)
        for (key, value) in flashvars.items():
            mobj = re.search('quality_(\\d+)[pP]', key)
            if mobj:
                extract_format(value, int(mobj.group(1)))
        video_url = flashvars.get('video_url')
        if (video_url and determine_ext(video_url, None)):
            extract_format(video_url)
    video_url = self._html_search_regex('flashvars\\.video_url\\s*=\\s*(["\\\'])(?P<url>http.+?)\\1', webpage, 'video url', default=None, group='url')
    if video_url:
        extract_format(compat_urllib_parse_unquote(video_url))
    if (not formats):
        if ('title="This video is no longer available"' in webpage):
            raise ExtractorError(('Video %s is no longer available' % video_id), expected=True)
    self._sort_formats(formats)
    if (not title):
        title = self._html_search_regex('<h1[^>]*>([^<]+)', webpage, 'title')
    return (webpage, {
        'id': video_id,
        'display_id': display_id,
        'title': strip_or_none(title),
        'thumbnail': thumbnail,
        'duration': duration,
        'age_limit': 18,
        'formats': formats,
    })