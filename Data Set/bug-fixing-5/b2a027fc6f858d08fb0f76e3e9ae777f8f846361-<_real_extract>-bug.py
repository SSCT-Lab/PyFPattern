def _real_extract(self, url):
    video_id = self._match_id(url)
    webpage = self._download_webpage(url, video_id)
    video_url = self._search_regex('(?s)<div[^>]+class=["\\\']page-diffusion["\\\'][^>]*>.*?<button[^>]+data-url=(["\\\'])(?P<url>(?:(?!\\1).)+)\\1', webpage, 'video url', group='url')
    title = self._og_search_title(webpage)
    description = self._og_search_description(webpage)
    upload_date_str = self._search_regex('class=["\\\']cover-emission-period["\\\'][^>]*>[^<]+\\s+(\\d{1,2}\\s+[^\\s]+\\s+\\d{4})<', webpage, 'upload date', fatal=False)
    if upload_date_str:
        upload_date_list = upload_date_str.split()
        upload_date_list.reverse()
        upload_date_list[1] = ('%02d' % (month_by_name(upload_date_list[1], lang='fr') or 0))
        upload_date_list[2] = ('%02d' % int(upload_date_list[2]))
        upload_date = ''.join(upload_date_list)
    else:
        upload_date = None
    return {
        'id': video_id,
        'title': title,
        'description': description,
        'upload_date': upload_date,
        'formats': [{
            'url': video_url,
            'vcodec': 'none',
        }],
    }