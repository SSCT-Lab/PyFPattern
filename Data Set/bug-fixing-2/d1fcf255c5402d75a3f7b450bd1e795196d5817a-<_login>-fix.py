

def _login(self):
    (username, password) = self._get_login_info()
    if (username is None):
        return
    (_, urlh) = self._download_webpage_handle('https://learning.oreilly.com/accounts/login-check/', None, 'Downloading login page')

    def is_logged(urlh):
        return ('learning.oreilly.com/home/' in compat_str(urlh.geturl()))
    if is_logged(urlh):
        self.LOGGED_IN = True
        return
    redirect_url = compat_str(urlh.geturl())
    parsed_url = compat_urlparse.urlparse(redirect_url)
    qs = compat_parse_qs(parsed_url.query)
    next_uri = compat_urlparse.urljoin('https://api.oreilly.com', qs['next'][0])
    (auth, urlh) = self._download_json_handle('https://www.oreilly.com/member/auth/login/', None, 'Logging in', data=json.dumps({
        'email': username,
        'password': password,
        'redirect_uri': next_uri,
    }).encode(), headers={
        'Content-Type': 'application/json',
        'Referer': redirect_url,
    }, expected_status=400)
    credentials = auth.get('credentials')
    if ((not auth.get('logged_in')) and (not auth.get('redirect_uri')) and credentials):
        raise ExtractorError(('Unable to login: %s' % credentials), expected=True)
    for cookie in ('groot_sessionid', 'orm-jwt', 'orm-rt'):
        self._apply_first_set_cookie_header(urlh, cookie)
    (_, urlh) = self._download_webpage_handle((auth.get('redirect_uri') or next_uri), None, 'Completing login')
    if is_logged(urlh):
        self.LOGGED_IN = True
        return
    raise ExtractorError('Unable to log in')
