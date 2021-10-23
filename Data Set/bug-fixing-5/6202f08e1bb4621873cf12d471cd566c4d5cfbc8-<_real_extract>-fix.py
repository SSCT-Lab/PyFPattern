def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    title = self._html_search_meta('fulltitle', webpage, default=None)
    if ((not title) or (title == "c't")):
        title = self._search_regex('<div[^>]+class="videoplayerjw"[^>]+data-title="([^"]+)"', webpage, 'title')
    yt_urls = YoutubeIE._extract_urls(webpage)
    if yt_urls:
        return self.playlist_from_matches(yt_urls, video_id, title, ie=YoutubeIE.ie_key())
    kaltura_url = KalturaIE._extract_url(webpage)
    if kaltura_url:
        return self.url_result(smuggle_url(kaltura_url, {
            'source_url': url,
        }), KalturaIE.ie_key())
    container_id = self._search_regex('<div class="videoplayerjw"[^>]+data-container="([0-9]+)"', webpage, 'container ID')
    sequenz_id = self._search_regex('<div class="videoplayerjw"[^>]+data-sequenz="([0-9]+)"', webpage, 'sequenz ID')
    doc = self._download_xml('http://www.heise.de/videout/feed', video_id, query={
        'container': container_id,
        'sequenz': sequenz_id,
    })
    formats = []
    for source_node in doc.findall('.//{http://rss.jwpcdn.com/}source'):
        label = source_node.attrib['label']
        height = int_or_none(self._search_regex('^(.*?_)?([0-9]+)p$', label, 'height', default=None))
        video_url = source_node.attrib['file']
        ext = determine_ext(video_url, '')
        formats.append({
            'url': video_url,
            'format_note': label,
            'format_id': ('%s_%s' % (ext, label)),
            'height': height,
        })
    self._sort_formats(formats)
    description = (self._og_search_description(webpage, default=None) or self._html_search_meta('description', webpage))
    return {
        'id': video_id,
        'title': title,
        'description': description,
        'thumbnail': (xpath_text(doc, './/{http://rss.jwpcdn.com/}image') or self._og_search_thumbnail(webpage)),
        'timestamp': parse_iso8601(self._html_search_meta('date', webpage)),
        'formats': formats,
    }