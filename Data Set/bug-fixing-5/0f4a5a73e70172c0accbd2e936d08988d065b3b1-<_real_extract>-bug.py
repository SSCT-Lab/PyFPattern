def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = mobj.group('id')
    display_id = (mobj.group('display_id') or video_id)
    webpage = self._download_webpage(('http://www.drtuber.com/video/%s' % video_id), display_id)
    video_url = self._html_search_regex('<source src="([^"]+)"', webpage, 'video URL')
    title = self._html_search_regex(('class="title_watch"[^>]*><(?:p|h\\d+)[^>]*>([^<]+)<', '<p[^>]+class="title_substrate">([^<]+)</p>', '<title>([^<]+) - \\d+'), webpage, 'title')
    thumbnail = self._html_search_regex('poster="([^"]+)"', webpage, 'thumbnail', fatal=False)

    def extract_count(id_, name, default=NO_DEFAULT):
        return str_to_int(self._html_search_regex(('<span[^>]+(?:class|id)="%s"[^>]*>([\\d,\\.]+)</span>' % id_), webpage, ('%s count' % name), default=default, fatal=False))
    like_count = extract_count('rate_likes', 'like')
    dislike_count = extract_count('rate_dislikes', 'dislike', default=None)
    comment_count = extract_count('comments_count', 'comment')
    cats_str = self._search_regex('<div[^>]+class="categories_list">(.+?)</div>', webpage, 'categories', fatal=False)
    categories = ([] if (not cats_str) else re.findall('<a title="([^"]+)"', cats_str))
    return {
        'id': video_id,
        'display_id': display_id,
        'url': video_url,
        'title': title,
        'thumbnail': thumbnail,
        'like_count': like_count,
        'dislike_count': dislike_count,
        'comment_count': comment_count,
        'categories': categories,
        'age_limit': self._rta_search(webpage),
    }