def _json_ld(self, json_ld, video_id, fatal=True, expected_type=None):
    if isinstance(json_ld, compat_str):
        json_ld = self._parse_json(json_ld, video_id, fatal=fatal)
    if (not json_ld):
        return {
            
        }
    info = {
        
    }
    if (not isinstance(json_ld, (list, tuple, dict))):
        return info
    if isinstance(json_ld, dict):
        json_ld = [json_ld]

    def extract_video_object(e):
        assert (e['@type'] == 'VideoObject')
        info.update({
            'url': e.get('contentUrl'),
            'title': unescapeHTML(e.get('name')),
            'description': unescapeHTML(e.get('description')),
            'thumbnail': (e.get('thumbnailUrl') or e.get('thumbnailURL')),
            'duration': parse_duration(e.get('duration')),
            'timestamp': unified_timestamp(e.get('uploadDate')),
            'filesize': float_or_none(e.get('contentSize')),
            'tbr': int_or_none(e.get('bitrate')),
            'width': int_or_none(e.get('width')),
            'height': int_or_none(e.get('height')),
            'view_count': int_or_none(e.get('interactionCount')),
        })
    for e in json_ld:
        if (isinstance(e.get('@context'), compat_str) and re.match('^https?://schema.org/?$', e.get('@context'))):
            item_type = e.get('@type')
            if ((expected_type is not None) and (expected_type != item_type)):
                return info
            if (item_type in ('TVEpisode', 'Episode')):
                info.update({
                    'episode': unescapeHTML(e.get('name')),
                    'episode_number': int_or_none(e.get('episodeNumber')),
                    'description': unescapeHTML(e.get('description')),
                })
                part_of_season = e.get('partOfSeason')
                if (isinstance(part_of_season, dict) and (part_of_season.get('@type') in ('TVSeason', 'Season', 'CreativeWorkSeason'))):
                    info['season_number'] = int_or_none(part_of_season.get('seasonNumber'))
                part_of_series = (e.get('partOfSeries') or e.get('partOfTVSeries'))
                if (isinstance(part_of_series, dict) and (part_of_series.get('@type') in ('TVSeries', 'Series', 'CreativeWorkSeries'))):
                    info['series'] = unescapeHTML(part_of_series.get('name'))
            elif (item_type in ('Article', 'NewsArticle')):
                info.update({
                    'timestamp': parse_iso8601(e.get('datePublished')),
                    'title': unescapeHTML(e.get('headline')),
                    'description': unescapeHTML(e.get('articleBody')),
                })
            elif (item_type == 'VideoObject'):
                extract_video_object(e)
                continue
            video = e.get('video')
            if (isinstance(video, dict) and (video.get('@type') == 'VideoObject')):
                extract_video_object(video)
            break
    return dict(((k, v) for (k, v) in info.items() if (v is not None)))