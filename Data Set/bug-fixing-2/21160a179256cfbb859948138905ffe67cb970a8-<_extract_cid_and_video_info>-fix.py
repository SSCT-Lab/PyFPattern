

def _extract_cid_and_video_info(self, video_id):
    data = self._download_json(('%s/zapi/v2/cached/program/power_details/%s' % (self._HOST_URL, self._power_guide_hash)), video_id, 'Downloading video information', query={
        'program_ids': video_id,
        'complete': True,
    })
    p = data['programs'][0]
    cid = p['cid']
    info_dict = {
        'id': video_id,
        'title': (p.get('t') or p['et']),
        'description': p.get('d'),
        'thumbnail': p.get('i_url'),
        'creator': p.get('channel_name'),
        'episode': p.get('et'),
        'episode_number': int_or_none(p.get('e_no')),
        'season_number': int_or_none(p.get('s_no')),
        'release_year': int_or_none(p.get('year')),
        'categories': try_get(p, (lambda x: x['c']), list),
        'tags': try_get(p, (lambda x: x['g']), list),
    }
    return (cid, info_dict)
