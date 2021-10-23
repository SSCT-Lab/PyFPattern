

def _extract_clip(self, url, webpage):
    clip_id = self._html_search_regex(self._CLIPID_REGEXES, webpage, 'clip id')
    title = self._html_search_regex(self._TITLE_REGEXES, webpage, 'title')
    info = self._extract_video_info(url, clip_id)
    description = self._html_search_regex(self._DESCRIPTION_REGEXES, webpage, 'description', fatal=False)
    thumbnail = self._og_search_thumbnail(webpage)
    upload_date = unified_strdate(self._html_search_regex(self._UPLOAD_DATE_REGEXES, webpage, 'upload date', default=None))
    info.update({
        'id': clip_id,
        'title': title,
        'description': description,
        'thumbnail': thumbnail,
        'upload_date': upload_date,
    })
    return info
