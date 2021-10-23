

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('http://www.xvideos.com/video%s/' % video_id), video_id)
    mobj = re.search('<h1 class="inlineError">(.+?)</h1>', webpage)
    if mobj:
        raise ExtractorError(('%s said: %s' % (self.IE_NAME, clean_html(mobj.group(1)))), expected=True)
    title = (self._html_search_regex(('<title>(?P<title>.+?)\\s+-\\s+XVID', 'setVideoTitle\\s*\\(\\s*(["\\\'])(?P<title>(?:(?!\\1).)+)\\1'), webpage, 'title', default=None, group='title') or self._og_search_title(webpage))
    thumbnail = self._search_regex(('setThumbUrl\\(\\s*(["\\\'])(?P<thumbnail>(?:(?!\\1).)+)\\1', 'url_bigthumb=(?P<thumbnail>.+?)&amp'), webpage, 'thumbnail', fatal=False, group='thumbnail')
    duration = (int_or_none(self._og_search_property('duration', webpage, default=None)) or parse_duration(self._search_regex('<span[^>]+class=["\\\']duration["\\\'][^>]*>.*?(\\d[^<]+)', webpage, 'duration', fatal=False)))
    formats = []
    video_url = compat_urllib_parse_unquote(self._search_regex('flv_url=(.+?)&', webpage, 'video URL', default=''))
    if video_url:
        formats.append({
            'url': video_url,
            'format_id': 'flv',
        })
    for (kind, _, format_url) in re.findall('setVideo([^(]+)\\((["\\\'])(http.+?)\\2\\)', webpage):
        format_id = kind.lower()
        if (format_id == 'hls'):
            formats.extend(self._extract_m3u8_formats(format_url, video_id, 'mp4', entry_protocol='m3u8_native', m3u8_id='hls', fatal=False))
        elif (format_id in ('urllow', 'urlhigh')):
            formats.append({
                'url': format_url,
                'format_id': ('%s-%s' % (determine_ext(format_url, 'mp4'), format_id[3:])),
                'quality': ((- 2) if format_id.endswith('low') else None),
            })
    self._sort_formats(formats)
    return {
        'id': video_id,
        'formats': formats,
        'title': title,
        'duration': duration,
        'thumbnail': thumbnail,
        'age_limit': 18,
    }
