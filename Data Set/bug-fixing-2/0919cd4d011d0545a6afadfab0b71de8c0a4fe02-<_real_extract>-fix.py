

def _real_extract(self, url):
    display_id = self._match_id(url)
    webpage = self._download_webpage(url, display_id)
    video_data = self._parse_json(unescapeHTML(self._search_regex(['flashPlayerOptions\\s*=\\s*(["\\\'])(?P<json>(?:(?!\\1).)+)\\1', 'class="[^"]*jsb_video/FlashPlayer[^"]*"[^>]+data-jsb="(?P<json>[^"]+)"'], webpage, 'player data', group='json')), display_id)['config']['initial_video']
    video_id = video_data['id']
    video_title = video_data['title']
    parts = []
    for part in video_data.get('parts', []):
        part_id = part['id']
        part_title = part['title']
        formats = []
        for source in part.get('sources', []):
            source_url = source.get('src')
            if (not source_url):
                continue
            ext = determine_ext(source_url)
            if (ext == 'm3u8'):
                formats.extend(self._extract_m3u8_formats(source_url, part_id, 'mp4', 'm3u8_native', m3u8_id='hls', fatal=False))
            else:
                formats.append({
                    'format_id': source.get('delivery'),
                    'url': source_url,
                })
        self._sort_formats(formats)
        parts.append({
            'id': part_id,
            'title': part_title,
            'thumbnail': part.get('preview_image_url'),
            'duration': int_or_none(part.get('duration')),
            'is_live': part.get('is_livestream'),
            'formats': formats,
        })
    return {
        '_type': 'multi_video',
        'id': video_id,
        'title': video_title,
        'entries': parts,
    }
