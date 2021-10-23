def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    urplayer_data = self._parse_json(self._search_regex('urPlayer\\.init\\(({.+?})\\);', webpage, 'urplayer data'), video_id)
    host = self._download_json('http://streaming-loadbalancer.ur.se/loadbalancer.json', video_id)['redirect']
    formats = []
    for (quality_attr, quality, preference) in (('', 'sd', 0), ('_hd', 'hd', 1)):
        file_http = (urplayer_data.get(('file_http' + quality_attr)) or urplayer_data.get(('file_http_sub' + quality_attr)))
        if file_http:
            formats.extend(self._extract_wowza_formats(('http://%s/%splaylist.m3u8' % (host, file_http)), video_id, skip_protocols=['rtmp', 'rtsp']))
    self._sort_formats(formats)
    subtitles = {
        
    }
    for subtitle in urplayer_data.get('subtitles', []):
        subtitle_url = subtitle.get('file')
        kind = subtitle.get('kind')
        if ((not subtitle_url) or (kind and (kind != 'captions'))):
            continue
        subtitles.setdefault(subtitle.get('label', 'Svenska'), []).append({
            'url': subtitle_url,
        })
    return {
        'id': video_id,
        'title': urplayer_data['title'],
        'description': self._og_search_description(webpage),
        'thumbnail': urplayer_data.get('image'),
        'series': urplayer_data.get('series_title'),
        'subtitles': subtitles,
        'formats': formats,
    }