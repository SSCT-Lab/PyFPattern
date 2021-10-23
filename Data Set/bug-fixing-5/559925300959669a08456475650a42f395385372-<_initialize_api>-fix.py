def _initialize_api(self, video_id):
    post_data = json.dumps({
        'client_id': 'SPupX1tvqFEopQ1YS6SS',
        'grant_type': 'urn:vevo:params:oauth:grant-type:anonymous',
    }).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
    }
    req = sanitized_Request('https://accounts.vevo.com/token', post_data, headers)
    webpage = self._download_webpage(req, None, note='Retrieving oauth token', errnote='Unable to retrieve oauth token')
    if re.search('(?i)THIS PAGE IS CURRENTLY UNAVAILABLE IN YOUR REGION', webpage):
        self.raise_geo_restricted(('%s said: This page is currently unavailable in your region' % self.IE_NAME))
    auth_info = self._parse_json(webpage, video_id)
    self._api_url_template = ((self.http_scheme() + '//apiv2.vevo.com/%s?token=') + auth_info['legacy_token'])