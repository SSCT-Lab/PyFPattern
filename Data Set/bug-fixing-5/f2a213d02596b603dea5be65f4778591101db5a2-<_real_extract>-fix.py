def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    host = mobj.group('host')
    video_id = mobj.group('id')
    webpage = self._download_webpage(url, video_id)
    title = self._html_search_regex('<h3>([^<]+)</h3>', webpage, 'title')
    player_params = extract_attributes(self._search_regex('(<section[^>]+id="UIVideoPlayer"[^>]+>)', webpage, 'player parameters'))
    page_id = self._html_search_regex('<html[^>]+data-pageid="([^"]+)"', webpage, 'page ID')
    video_data = self._download_json(('https://%s/ajax/movie/watch/%s/' % (host, video_id)), video_id, data=urlencode_postdata({
        'xEvent': 'UIVideoPlayer.PingOutcome',
        'xJson': json.dumps({
            'EJOutcomes': player_params['data-ejpingables'],
            'NativeHLS': False,
        }),
        'arcVersion': 3,
        'appVersion': 59,
        'gorilla.csrf.Token': page_id,
    }))['Data']
    if (isinstance(video_data, compat_str) and video_data.startswith('/ratelimited/')):
        raise ExtractorError('Download rate reached. Please try again later.', expected=True)
    ej_links = self._decrypt(video_data['EJLinks'], video_id)
    formats = []
    m3u8_url = ej_links.get('HLSLink')
    if m3u8_url:
        formats.extend(self._extract_m3u8_formats(m3u8_url, video_id, ext='mp4', entry_protocol='m3u8_native'))
    mp4_url = ej_links.get('MP4Link')
    if mp4_url:
        formats.append({
            'url': mp4_url,
        })
    self._sort_formats(formats)
    description = get_elements_by_class('synopsis', webpage)[0]
    thumbnail = self._html_search_regex('<img[^>]+src=(["\'])(?P<url>(?!\\1).+?/moviecovers/(?!\\1).+?)\\1', webpage, 'thumbnail url', fatal=False, group='url')
    if (thumbnail is not None):
        thumbnail = compat_urlparse.urljoin(url, thumbnail)
    return {
        'id': video_id,
        'title': title,
        'formats': formats,
        'thumbnail': thumbnail,
        'description': description,
    }