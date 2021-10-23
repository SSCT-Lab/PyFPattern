

def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(('https://openload.co/embed/%s/' % video_id), video_id)
    if (('File not found' in webpage) or ('deleted by the owner' in webpage)):
        raise ExtractorError('File not found', expected=True)
    ol_id = self._search_regex('<span[^>]+id="[^"]+"[^>]*>([0-9A-Za-z]+)</span>', webpage, 'openload ID')
    video_url_chars = []
    first_char = ord(ol_id[0])
    key = (first_char - 50)
    maxKey = max(2, key)
    key = min(maxKey, (len(ol_id) - 22))
    t = ol_id[key:(key + 20)]
    hashMap = {
        
    }
    v = ol_id.replace(t, '')
    h = 0
    while (h < len(t)):
        f = t[h:(h + 2)]
        i = int(f, 16)
        hashMap[(h / 2)] = i
        h += 2
    h = 0
    while (h < len(v)):
        B = v[h:(h + 3)]
        i = int(B, 16)
        if (((h / 3) % 3) == 0):
            i = int(B, 8)
        index = ((h / 3) % 10)
        A = hashMap[index]
        i = (i ^ 47)
        i = (i ^ A)
        video_url_chars.append(compat_chr(i))
        h += 3
    video_url = 'https://openload.co/stream/%s?mime=true'
    video_url = (video_url % ''.join(video_url_chars))
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
