

def _real_extract(self, url):
    video_id = self._match_id(url)
    self._set_cookie('91porn.com', 'language', 'cn_CN')
    webpage = self._download_webpage(('http://91porn.com/view_video.php?viewkey=%s' % video_id), video_id)
    if ('作为游客，你每天只可观看10个视频' in webpage):
        raise ExtractorError('91 Porn says: Daily limit 10 videos exceeded', expected=True)
    title = self._search_regex('<div id="viewvideo-title">([^<]+)</div>', webpage, 'title')
    title = title.replace('\n', '')
    video_link_url = self._search_regex('<textarea[^>]+id=["\\\']fm-video_link[^>]+>([^<]+)</textarea>', webpage, 'video link')
    videopage = self._download_webpage(video_link_url, video_id)
    info_dict = self._parse_html5_media_entries(url, videopage, video_id)[0]
    duration = parse_duration(self._search_regex('时长:\\s*</span>\\s*(\\d+:\\d+)', webpage, 'duration', fatal=False))
    comment_count = int_or_none(self._search_regex('留言:\\s*</span>\\s*(\\d+)', webpage, 'comment count', fatal=False))
    info_dict.update({
        'id': video_id,
        'title': title,
        'duration': duration,
        'comment_count': comment_count,
        'age_limit': self._rta_search(webpage),
    })
    return info_dict
