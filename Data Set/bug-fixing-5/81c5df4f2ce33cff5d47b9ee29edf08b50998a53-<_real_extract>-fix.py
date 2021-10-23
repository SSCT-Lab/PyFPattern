def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('http://vidzi.tv/%s' % video_id), video_id)
    title = self._html_search_regex('(?s)<h2 class="video-title">(.*?)</h2>', webpage, 'title')
    codes = [webpage]
    codes.extend([decode_packed_codes(mobj.group(0)).replace("\\'", "'") for mobj in re.finditer(PACKED_CODES_RE, webpage)])
    for (num, code) in enumerate(codes, 1):
        jwplayer_data = self._parse_json(self._search_regex('setup\\(([^)]+)\\)', code, 'jwplayer data', default=(NO_DEFAULT if (num == len(codes)) else '{}')), video_id, transform_source=(lambda s: js_to_json(re.sub('\\s*\\+\\s*window\\[.+?\\]', '', s))))
        if jwplayer_data:
            break
    info_dict = self._parse_jwplayer_data(jwplayer_data, video_id, require_title=False)
    info_dict['title'] = title
    return info_dict