def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('https://openload.co/embed/%s/' % video_id), video_id)
    if (('File not found' in webpage) or ('deleted by the owner' in webpage)):
        raise ExtractorError('File not found', expected=True)
    ol_id = self._search_regex('<span[^>]+id="[^"]+"[^>]*>([0-9A-Za-z]+)</span>', webpage, 'openload ID')
    first_char = int(ol_id[0])
    urlcode = []
    num = 1
    while (num < len(ol_id)):
        i = ord(ol_id[num])
        key = 0
        if (i <= 90):
            key = (i - 65)
        elif (i >= 97):
            key = ((25 + i) - 97)
        urlcode.append((key, compat_chr(((int(ol_id[(num + 2):(num + 5)]) // int(ol_id[(num + 1)])) - first_char))))
        num += 5
    video_url = ('https://openload.co/stream/' + ''.join([value for (_, value) in sorted(urlcode, key=(lambda x: x[0]))]))
    title = (self._og_search_title(webpage, default=None) or self._search_regex('<span[^>]+class=["\\\']title["\\\'][^>]*>([^<]+)', webpage, 'title', default=None) or self._html_search_meta('description', webpage, 'title', fatal=True))
    entries = self._parse_html5_media_entries(url, webpage, video_id)
    subtitles = (entries[0]['subtitles'] if entries else None)
    info_dict = {
        'id': video_id,
        'title': title,
        'thumbnail': self._og_search_thumbnail(webpage, default=None),
        'url': video_url,
        'ext': determine_ext(title, 'mp4'),
        'subtitles': subtitles,
    }
    return info_dict