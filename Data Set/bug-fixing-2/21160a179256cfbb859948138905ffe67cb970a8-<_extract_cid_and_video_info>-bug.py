

def _extract_cid_and_video_info(self, video_id):
    data = self._download_json(('%s/zapi/program/details' % self._HOST_URL), video_id, 'Downloading video information', query={
        'program_id': video_id,
        'complete': True,
    })
    p = data['program']
    cid = p['cid']
    info_dict = {
        'id': video_id,
        'title': (p.get('title') or p['episode_title']),
        'description': p.get('description'),
        'thumbnail': p.get('image_url'),
        'creator': p.get('channel_name'),
        'episode': p.get('episode_title'),
        'episode_number': int_or_none(p.get('episode_number')),
        'season_number': int_or_none(p.get('season_number')),
        'release_year': int_or_none(p.get('year')),
        'categories': try_get(p, (lambda x: x['categories']), list),
    }
    return (cid, info_dict)
