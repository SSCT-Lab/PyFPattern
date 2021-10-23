

def _real_extract(self, url):
    display_id = self._match_id(url)
    webpage = self._download_webpage(url, display_id)
    formats = []
    quality = qualities(['ld', 'md', 'hd'])
    model = self._html_search_regex('data-model="([^"]+)"', webpage, 'data model', default=None)
    if model:
        model_data = self._parse_json(model, display_id)
        for video_url in model_data['sources'].values():
            (video_id, format_id) = url_basename(video_url).split('_')[:2]
            formats.append({
                'format_id': format_id,
                'quality': quality(format_id),
                'url': video_url,
            })
        title = model_data['title']
    else:
        video_id = display_id
        media_data = self._download_json(('http://www.allocine.fr/ws/AcVisiondataV5.ashx?media=%s' % video_id), display_id)
        for (key, value) in media_data['video'].items():
            if (not key.endswith('Path')):
                continue
            format_id = key[:(- len('Path'))]
            formats.append({
                'format_id': format_id,
                'quality': quality(format_id),
                'url': value,
            })
        title = remove_end(self._html_search_regex('(?s)<title>(.+?)</title>', webpage, 'title').strip(), ' - AlloCiné')
    self._sort_formats(formats)
    return {
        'id': video_id,
        'display_id': display_id,
        'title': title,
        'thumbnail': self._og_search_thumbnail(webpage),
        'formats': formats,
        'description': self._og_search_description(webpage),
    }
