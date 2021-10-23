def send(self, path, data, **kwargs):
    '\n        Sends the command to the device over api\n        '
    url_kwargs = dict(timeout=self.get_option('timeout'), validate_certs=self.get_option('validate_certs'), headers={
        
    })
    url_kwargs.update(kwargs)
    if self._auth:
        headers = dict(kwargs.get('headers', {
            
        }))
        headers.update(self._auth)
        url_kwargs['headers'] = headers
    else:
        url_kwargs['force_basic_auth'] = True
        url_kwargs['url_username'] = self.get_option('remote_user')
        url_kwargs['url_password'] = self.get_option('password')
    try:
        url = (self._url + path)
        self._log_messages(("send url '%s' with data '%s' and kwargs '%s'" % (url, data, url_kwargs)))
        response = open_url(url, data=data, **url_kwargs)
    except HTTPError as exc:
        is_handled = self.handle_httperror(exc)
        if (is_handled is True):
            return self.send(path, data, **kwargs)
        elif (is_handled is False):
            raise
        else:
            response = is_handled
    except URLError as exc:
        raise AnsibleConnectionFailure('Could not connect to {0}: {1}'.format((self._url + path), exc.reason))
    response_buffer = BytesIO()
    resp_data = response.read()
    self._log_messages(("received response: '%s'" % resp_data))
    response_buffer.write(resp_data)
    self._auth = (self.update_auth(response, response_buffer) or self._auth)
    response_buffer.seek(0)
    return (response, response_buffer)