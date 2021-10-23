

def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    (video_id, site_id) = mobj.group('id', 'site_id')
    webpage = self._download_webpage(url, video_id)
    config = self._parse_json(self._search_regex("videoJSConfig\\s*=\\s*JSON\\.parse\\(\\'({.+?})\\'\\);", webpage, 'config', default='{}'), video_id, transform_source=(lambda s: s.replace('\\\\', '\\').replace('\\"', '"').replace("\\'", "'")))
    vod_id = (config.get('vodId') or self._search_regex(('\\\\"vodId\\\\"\\s*:\\s*\\\\"(.+?)\\\\"', '<[^>]+id=["\\\']vod-(\\d+)'), webpage, 'video_id', default=None))
    if (not vod_id):
        player = self._parse_json(self._search_regex('vmmaplayer\\(({.+?})\\);', webpage, 'vmma player', default=''), video_id, transform_source=(lambda s: ('[%s]' % s)), fatal=False)
        if player:
            video = player[(- 1)]
            if (video['videoUrl'] in ('http', 'https')):
                return self.url_result(video['url'], MedialaanIE.ie_key())
            info = {
                'id': video_id,
                'url': video['videoUrl'],
                'title': video['title'],
                'thumbnail': video.get('imageUrl'),
                'timestamp': int_or_none(video.get('createdDate')),
                'duration': int_or_none(video.get('duration')),
            }
        else:
            info = self._parse_html5_media_entries(url, webpage, video_id, m3u8_id='hls')[0]
            info.update({
                'id': video_id,
                'title': self._html_search_meta('description', webpage),
                'duration': parse_duration(self._html_search_meta('duration', webpage)),
            })
    else:
        if (not self._logged_in):
            self._login()
        settings = self._parse_json(self._search_regex('jQuery\\.extend\\(Drupal\\.settings\\s*,\\s*({.+?})\\);', webpage, 'drupal settings', default='{}'), video_id)

        def get(container, item):
            return (try_get(settings, (lambda x: x[container][item]), compat_str) or self._search_regex(('"%s"\\s*:\\s*"([^"]+)' % item), webpage, item, default=None))
        app_id = (get('vod', 'app_id') or self._SITE_TO_APP_ID.get(site_id, 'vtm_watch'))
        sso = (get('vod', 'gigyaDatabase') or 'vtm-sso')
        data = self._download_json(('http://vod.medialaan.io/api/1.0/item/%s/video' % vod_id), video_id, query={
            'app_id': app_id,
            'user_network': sso,
            'UID': self._uid,
            'UIDSignature': self._uid_signature,
            'signatureTimestamp': self._signature_timestamp,
        })
        formats = self._extract_m3u8_formats(data['response']['uri'], video_id, entry_protocol='m3u8_native', ext='mp4', m3u8_id='hls')
        self._sort_formats(formats)
        info = {
            'id': vod_id,
            'formats': formats,
        }
        api_key = get('vod', 'apiKey')
        channel = get('medialaanGigya', 'channel')
        if api_key:
            videos = self._download_json('http://vod.medialaan.io/vod/v2/videos', video_id, fatal=False, query={
                'channels': channel,
                'ids': vod_id,
                'limit': 1,
                'apikey': api_key,
            })
            if videos:
                video = try_get(videos, (lambda x: x['response']['videos'][0]), dict)
                if video:

                    def get(container, item, expected_type=None):
                        return try_get(video, (lambda x: x[container][item]), expected_type)

                    def get_string(container, item):
                        return get(container, item, compat_str)
                    info.update({
                        'series': get_string('program', 'title'),
                        'season': get_string('season', 'title'),
                        'season_number': int_or_none(get('season', 'number')),
                        'season_id': get_string('season', 'id'),
                        'episode': get_string('episode', 'title'),
                        'episode_number': int_or_none(get('episode', 'number')),
                        'episode_id': get_string('episode', 'id'),
                        'duration': (int_or_none(video.get('duration')) or int_or_none(video.get('durationMillis'), scale=1000)),
                        'title': get_string('episode', 'title'),
                        'description': get_string('episode', 'text'),
                        'timestamp': unified_timestamp(get_string('publication', 'begin')),
                    })
        if (not info.get('title')):
            info['title'] = (try_get(config, (lambda x: x['videoConfig']['title']), compat_str) or self._html_search_regex('\\\\"title\\\\"\\s*:\\s*\\\\"(.+?)\\\\"', webpage, 'title', default=None) or self._og_search_title(webpage))
    if (not info.get('description')):
        info['description'] = self._html_search_regex('<div[^>]+class="field-item\\s+even">\\s*<p>(.+?)</p>', webpage, 'description', default=None)
    return info
