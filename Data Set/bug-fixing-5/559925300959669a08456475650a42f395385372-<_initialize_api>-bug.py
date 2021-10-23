def _initialize_api(self, video_id):
    req = sanitized_Request('http://www.vevo.com/auth', data=b'')
    webpage = self._download_webpage(req, None, note='Retrieving oauth token', errnote='Unable to retrieve oauth token')
    if re.search('(?i)THIS PAGE IS CURRENTLY UNAVAILABLE IN YOUR REGION', webpage):
        self.raise_geo_restricted(('%s said: This page is currently unavailable in your region' % self.IE_NAME))
    auth_info = self._parse_json(webpage, video_id)
    self._api_url_template = ((self.http_scheme() + '//apiv2.vevo.com/%s?token=') + auth_info['access_token'])