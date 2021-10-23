

def _extract_wdr_video(self, webpage, display_id):
    json_metadata = self._html_search_regex('class=(?:"(?:mediaLink|wdrrPlayerPlayBtn|videoButton)\\b[^"]*"[^>]+|"videoLink\\b[^"]*"[\\s]*>\\n[^\\n]*)data-extension="([^"]+)"', webpage, 'media link', default=None, flags=re.MULTILINE)
    if (not json_metadata):
        return
    media_link_obj = self._parse_json(json_metadata, display_id, transform_source=js_to_json)
    jsonp_url = media_link_obj['mediaObj']['url']
    metadata = self._download_json(jsonp_url, 'metadata', transform_source=strip_jsonp)
    metadata_tracker_data = metadata['trackerData']
    metadata_media_resource = metadata['mediaResource']
    formats = []
    for (kind, media_resource) in metadata_media_resource.items():
        if (kind not in ('dflt', 'alt')):
            continue
        for (tag_name, medium_url) in media_resource.items():
            if (tag_name not in ('videoURL', 'audioURL')):
                continue
            ext = determine_ext(medium_url)
            if (ext == 'm3u8'):
                formats.extend(self._extract_m3u8_formats(medium_url, display_id, 'mp4', 'm3u8_native', m3u8_id='hls'))
            elif (ext == 'f4m'):
                manifest_url = update_url_query(medium_url, {
                    'hdcore': '3.2.0',
                    'plugin': 'aasp-3.2.0.77.18',
                })
                formats.extend(self._extract_f4m_formats(manifest_url, display_id, f4m_id='hds', fatal=False))
            elif (ext == 'smil'):
                formats.extend(self._extract_smil_formats(medium_url, 'stream', fatal=False))
            else:
                a_format = {
                    'url': medium_url,
                }
                if (ext == 'unknown_video'):
                    urlh = self._request_webpage(medium_url, display_id, note='Determining extension')
                    ext = urlhandle_detect_ext(urlh)
                    a_format['ext'] = ext
                formats.append(a_format)
    self._sort_formats(formats)
    subtitles = {
        
    }
    caption_url = metadata_media_resource.get('captionURL')
    if caption_url:
        subtitles['de'] = [{
            'url': caption_url,
            'ext': 'ttml',
        }]
    title = metadata_tracker_data['trackerClipTitle']
    return {
        'id': metadata_tracker_data.get('trackerClipId', display_id),
        'display_id': display_id,
        'title': title,
        'alt_title': metadata_tracker_data.get('trackerClipSubcategory'),
        'formats': formats,
        'subtitles': subtitles,
        'upload_date': unified_strdate(metadata_tracker_data.get('trackerClipAirTime')),
    }
