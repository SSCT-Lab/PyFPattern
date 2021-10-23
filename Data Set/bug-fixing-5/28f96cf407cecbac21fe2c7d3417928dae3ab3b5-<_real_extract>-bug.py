def _real_extract(self, url):
    (domain, video_id) = re.search(self._VALID_URL, url).groups()
    (service, consumer_name) = {
        '6play.fr': ('6play', 'm6web'),
        'rtlplay.be': ('rtlbe_rtl_play', 'rtlbe'),
    }.get(domain, ('6play', 'm6web'))
    data = self._download_json(('https://pc.middleware.6play.fr/6play/v2/platforms/m6group_web/services/%s/videos/clip_%s' % (service, video_id)), video_id, headers={
        'x-customer-name': consumer_name,
    }, query={
        'csa': 5,
        'with': 'clips',
    })
    clip_data = data['clips'][0]
    title = clip_data['title']
    urls = []
    quality_key = qualities(['lq', 'sd', 'hq', 'hd'])
    formats = []
    subtitles = {
        
    }
    for asset in clip_data['assets']:
        asset_url = asset.get('full_physical_path')
        protocol = asset.get('protocol')
        if ((not asset_url) or (protocol == 'primetime') or (asset_url in urls)):
            continue
        urls.append(asset_url)
        container = asset.get('video_container')
        ext = determine_ext(asset_url)
        if ((protocol == 'http_subtitle') or (ext == 'vtt')):
            subtitles.setdefault('fr', []).append({
                'url': asset_url,
            })
            continue
        if ((container == 'm3u8') or (ext == 'm3u8')):
            if (protocol == 'usp'):
                if compat_parse_qs(compat_urllib_parse_urlparse(asset_url).query).get('token', [None])[0]:
                    urlh = self._request_webpage(asset_url, video_id, fatal=False, headers=self.geo_verification_headers())
                    if (not urlh):
                        continue
                    asset_url = urlh.geturl()
                asset_url = re.sub('/([^/]+)\\.ism/[^/]*\\.m3u8', '/\\1.ism/\\1.m3u8', asset_url)
                formats.extend(self._extract_m3u8_formats(asset_url, video_id, 'mp4', 'm3u8_native', m3u8_id='hls', fatal=False))
                formats.extend(self._extract_f4m_formats(asset_url.replace('.m3u8', '.f4m'), video_id, f4m_id='hds', fatal=False))
                formats.extend(self._extract_mpd_formats(asset_url.replace('.m3u8', '.mpd'), video_id, mpd_id='dash', fatal=False))
                formats.extend(self._extract_ism_formats(re.sub('/[^/]+\\.m3u8', '/Manifest', asset_url), video_id, ism_id='mss', fatal=False))
            else:
                formats.extend(self._extract_m3u8_formats(asset_url, video_id, 'mp4', 'm3u8_native', m3u8_id='hls', fatal=False))
        elif ((container == 'mp4') or (ext == 'mp4')):
            quality = asset.get('video_quality')
            formats.append({
                'url': asset_url,
                'format_id': quality,
                'quality': quality_key(quality),
                'ext': ext,
            })
    self._sort_formats(formats)

    def get(getter):
        for src in (data, clip_data):
            v = try_get(src, getter, compat_str)
            if v:
                return v
    return {
        'id': video_id,
        'title': title,
        'description': get((lambda x: x['description'])),
        'duration': int_or_none(clip_data.get('duration')),
        'series': get((lambda x: x['program']['title'])),
        'formats': formats,
        'subtitles': subtitles,
    }