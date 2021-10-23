def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    display_id = mobj.group('display_id')
    (webpage, urlh) = self._download_webpage_handle(url, display_id)
    if ('src=expired' in urlh.geturl()):
        raise ExtractorError('This video is expired.', expected=True)
    video_id = mobj.group('video_id')
    if (not video_id):
        video_id = self._html_search_regex(self._VIDEO_ID_REGEXES, webpage, 'video id')
    data = None
    preload_codes = self._html_search_regex('(function.+)setTimeout\\(function\\(\\)\\{playlist', webpage, 'preload codes')
    base64_fragments = re.findall('"([a-zA-Z0-9+/=]+)"', preload_codes)
    base64_fragments.remove('init')

    def _check_sequence(cur_fragments):
        if (not cur_fragments):
            return
        for i in range(len(cur_fragments)):
            cur_sequence = ''.join((cur_fragments[i:] + cur_fragments[:i])).encode('ascii')
            try:
                raw_data = base64.b64decode(cur_sequence)
                if (compat_ord(raw_data[0]) == compat_ord('{')):
                    return json.loads(raw_data.decode('utf-8'))
            except (TypeError, binascii.Error, UnicodeDecodeError, ValueError):
                continue

    def _check_data():
        for i in range((len(base64_fragments) + 1)):
            for j in range(i, (len(base64_fragments) + 1)):
                data = _check_sequence((base64_fragments[:i] + base64_fragments[j:]))
                if data:
                    return data
    self.to_screen('Try to compute possible data sequence. This may take some time.')
    data = _check_data()
    if (not data):
        raise ExtractorError('Preload information could not be extracted', expected=True)
    formats = []
    get_quality = qualities(['500k', '480p', '1000k', '720p', '1080p'])
    for filed in data['files']:
        if (determine_ext(filed['url']) == 'm3u8'):
            if filed['url'].startswith('/'):
                m3u8_url = ('http://ht.cdn.turner.com/tbs/big/teamcoco' + filed['url'])
            else:
                m3u8_url = filed['url']
            m3u8_formats = self._extract_m3u8_formats(m3u8_url, video_id, ext='mp4')
            for m3u8_format in m3u8_formats:
                if (m3u8_format not in formats):
                    formats.append(m3u8_format)
        elif (determine_ext(filed['url']) == 'f4m'):
            continue
        else:
            if filed['url'].startswith('/mp4:protected/'):
                continue
            m_format = re.search('(\\d+(k|p))\\.mp4', filed['url'])
            if (m_format is not None):
                format_id = m_format.group(1)
            else:
                format_id = filed['bitrate']
            tbr = (int(filed['bitrate']) if filed['bitrate'].isdigit() else None)
            formats.append({
                'url': filed['url'],
                'ext': 'mp4',
                'tbr': tbr,
                'format_id': format_id,
                'quality': get_quality(format_id),
            })
    self._sort_formats(formats)
    return {
        'id': video_id,
        'display_id': display_id,
        'formats': formats,
        'title': data['title'],
        'thumbnail': data.get('thumb', {
            
        }).get('href'),
        'description': data.get('teaser'),
        'duration': data.get('duration'),
        'age_limit': self._family_friendly_search(webpage),
    }