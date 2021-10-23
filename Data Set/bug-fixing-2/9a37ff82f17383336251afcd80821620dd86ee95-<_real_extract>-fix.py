

def _real_extract(self, url):
    video_id = self._match_id(url)
    try:
        api_data = self._download_json('https://pcweb.api.mgtv.com/player/video', video_id, query={
            'tk2': base64.urlsafe_b64encode((b'did=%s|pno=1030|ver=0.3.0301|clit=%d' % (compat_str(uuid.uuid4()).encode(), time.time())))[::(- 1)],
            'video_id': video_id,
        }, headers=self.geo_verification_headers())['data']
    except ExtractorError as e:
        if (isinstance(e.cause, compat_HTTPError) and (e.cause.code == 401)):
            error = self._parse_json(e.cause.read().decode(), None)
            if (error.get('code') == 40005):
                self.raise_geo_restricted(countries=self._GEO_COUNTRIES)
            raise ExtractorError(error['msg'], expected=True)
        raise
    info = api_data['info']
    title = info['title'].strip()
    stream_data = self._download_json('https://pcweb.api.mgtv.com/player/getSource', video_id, query={
        'pm2': api_data['atc']['pm2'],
        'video_id': video_id,
    }, headers=self.geo_verification_headers())['data']
    stream_domain = stream_data['stream_domain'][0]
    formats = []
    for (idx, stream) in enumerate(stream_data['stream']):
        stream_path = stream.get('url')
        if (not stream_path):
            continue
        format_data = self._download_json((stream_domain + stream_path), video_id, note=('Download video info for format #%d' % idx))
        format_url = format_data.get('info')
        if (not format_url):
            continue
        tbr = int_or_none((stream.get('filebitrate') or self._search_regex('_(\\d+)_mp4/', format_url, 'tbr', default=None)))
        formats.append({
            'format_id': compat_str((tbr or idx)),
            'url': format_url,
            'ext': 'mp4',
            'tbr': tbr,
            'protocol': 'm3u8_native',
            'http_headers': {
                'Referer': url,
            },
            'format_note': stream.get('name'),
        })
    self._sort_formats(formats)
    return {
        'id': video_id,
        'title': title,
        'formats': formats,
        'description': info.get('desc'),
        'duration': int_or_none(info.get('duration')),
        'thumbnail': info.get('thumb'),
    }
