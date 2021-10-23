def _extract_playlist(self, channel_id):
    info = self._call_api(('kraken/channels/%s' % channel_id), channel_id, 'Downloading channel info JSON')
    channel_name = (info.get('display_name') or info.get('name'))
    entries = []
    offset = 0
    limit = self._PAGE_LIMIT
    broken_paging_detected = False
    counter_override = None
    for counter in itertools.count(1):
        response = self._call_api((self._PLAYLIST_PATH % (channel_id, offset, limit)), channel_id, ('Downloading %s JSON page %s' % (self._PLAYLIST_TYPE, (counter_override or counter))))
        page_entries = self._extract_playlist_page(response)
        if (not page_entries):
            break
        total = int_or_none(response.get('_total'))
        if ((not broken_paging_detected) and total and (len(page_entries) > limit)):
            self.report_warning('Twitch pagination is broken on twitch side, requesting all videos at once', channel_id)
            broken_paging_detected = True
            offset = total
            counter_override = '(all at once)'
            continue
        entries.extend(page_entries)
        if (broken_paging_detected or (total and (len(page_entries) >= total))):
            break
        offset += limit
    return self.playlist_result([self.url_result(entry) for entry in orderedSet(entries)], channel_id, channel_name)