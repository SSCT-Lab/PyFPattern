def _extract_entries(self, playlist_data_url, show_id, note, query):
    query['callback'] = 'cb'
    playlist_data = self._download_json(playlist_data_url, show_id, query=query, note=note, transform_source=(lambda s: js_to_json(strip_jsonp(s))))['html']
    drama_list = (get_element_by_class('p-drama-grid', playlist_data) or get_element_by_class('p-drama-half-row', playlist_data))
    if (drama_list is None):
        raise ExtractorError('No episodes found')
    video_urls = re.findall('<a[^>]+href="([^"]+)"', drama_list)
    return (playlist_data, [self.url_result(self._proto_relative_url(video_url, 'http:'), YoukuIE.ie_key()) for video_url in video_urls])