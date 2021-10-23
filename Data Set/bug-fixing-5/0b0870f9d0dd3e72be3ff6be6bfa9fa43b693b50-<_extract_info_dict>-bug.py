def _extract_info_dict(self, info, full_title=None, quiet=False, secret_token=None):
    track_id = compat_str(info['id'])
    name = (full_title or track_id)
    if quiet:
        self.report_extraction(name)
    thumbnail = info.get('artwork_url')
    if isinstance(thumbnail, compat_str):
        thumbnail = thumbnail.replace('-large', '-t500x500')
    ext = 'mp3'
    result = {
        'id': track_id,
        'uploader': info.get('user', {
            
        }).get('username'),
        'upload_date': unified_strdate(info.get('created_at')),
        'title': info['title'],
        'description': info.get('description'),
        'thumbnail': thumbnail,
        'duration': int_or_none(info.get('duration'), 1000),
        'webpage_url': info.get('permalink_url'),
        'license': info.get('license'),
    }
    formats = []
    query = {
        'client_id': self._CLIENT_ID,
    }
    if (secret_token is not None):
        query['secret_token'] = secret_token
    if info.get('downloadable', False):
        format_url = update_url_query(('https://api.soundcloud.com/tracks/%s/download' % track_id), query)
        formats.append({
            'format_id': 'download',
            'ext': info.get('original_format', 'mp3'),
            'url': format_url,
            'vcodec': 'none',
            'preference': 10,
        })
    format_dict = self._download_json(('https://api.soundcloud.com/i1/tracks/%s/streams' % track_id), track_id, 'Downloading track url', query=query)
    for (key, stream_url) in format_dict.items():
        abr = int_or_none(self._search_regex('_(\\d+)_url', key, 'audio bitrate', default=None))
        if key.startswith('http'):
            stream_formats = [{
                'format_id': key,
                'ext': ext,
                'url': stream_url,
            }]
        elif key.startswith('rtmp'):
            (url, path) = stream_url.split('mp3:', 1)
            stream_formats = [{
                'format_id': key,
                'url': url,
                'play_path': ('mp3:' + path),
                'ext': 'flv',
            }]
        elif key.startswith('hls'):
            stream_formats = self._extract_m3u8_formats(stream_url, track_id, 'mp3', entry_protocol='m3u8_native', m3u8_id=key, fatal=False)
        else:
            continue
        for f in stream_formats:
            f['abr'] = abr
        formats.extend(stream_formats)
    if (not formats):
        formats.append({
            'format_id': 'fallback',
            'url': update_url_query(info['stream_url'], query),
            'ext': ext,
        })
    for f in formats:
        f['vcodec'] = 'none'
    self._check_formats(formats, track_id)
    self._sort_formats(formats)
    result['formats'] = formats
    return result