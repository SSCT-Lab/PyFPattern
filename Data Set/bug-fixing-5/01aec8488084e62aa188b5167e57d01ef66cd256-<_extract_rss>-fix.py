def _extract_rss(self, url, video_id, doc):
    playlist_title = doc.find('./channel/title').text
    playlist_desc_el = doc.find('./channel/description')
    playlist_desc = (None if (playlist_desc_el is None) else playlist_desc_el.text)
    entries = []
    for it in doc.findall('./channel/item'):
        next_url = None
        enclosure_nodes = it.findall('./enclosure')
        for e in enclosure_nodes:
            next_url = e.attrib.get('url')
            if next_url:
                break
        if (not next_url):
            next_url = xpath_text(it, 'link', fatal=False)
        if (not next_url):
            continue
        entries.append({
            '_type': 'url_transparent',
            'url': next_url,
            'title': it.find('title').text,
        })
    return {
        '_type': 'playlist',
        'id': url,
        'title': playlist_title,
        'description': playlist_desc,
        'entries': entries,
    }