def get_entries_from_page(self, singmid):
    entries = []
    default_num = 1
    json_text = self.get_singer_all_songs(singmid, default_num)
    json_obj_all_songs = self._parse_json(json_text, singmid)
    if (json_obj_all_songs['code'] == 0):
        total = json_obj_all_songs['data']['total']
        json_text = self.get_singer_all_songs(singmid, total)
        json_obj_all_songs = self._parse_json(json_text, singmid)
    for item in json_obj_all_songs['data']['list']:
        if (item['musicData'].get('songmid') is not None):
            songmid = item['musicData']['songmid']
            entries.append(self.url_result(('https://y.qq.com/n/yqq/song/%s.html' % songmid), 'QQMusic', songmid))
    return entries