

def _extract_playlist(self, playlist_id):
    url = (self._TEMPLATE_URL % playlist_id)
    page = self._download_webpage(url, playlist_id)
    for match in re.findall('<div class="yt-alert-message">([^<]+)</div>', page):
        match = match.strip()
        if re.match('[^<]*(The|This) playlist (does not exist|is private)[^<]*', match):
            raise ExtractorError("The playlist doesn't exist or is private, use --username or --netrc to access it.", expected=True)
        elif re.match('[^<]*Invalid parameters[^<]*', match):
            raise ExtractorError('Invalid parameters. Maybe URL is incorrect.', expected=True)
        elif re.match('[^<]*Choose your language[^<]*', match):
            continue
        else:
            self.report_warning(('Youtube gives an alert message: ' + match))
    playlist_title = self._html_search_regex('(?s)<h1 class="pl-header-title[^"]*"[^>]*>\\s*(.*?)\\s*</h1>', page, 'title', default=None)
    has_videos = True
    if (not playlist_title):
        try:
            next(self._entries(page, playlist_id))
        except StopIteration:
            has_videos = False
    return (has_videos, self.playlist_result(self._entries(page, playlist_id), playlist_id, playlist_title))
