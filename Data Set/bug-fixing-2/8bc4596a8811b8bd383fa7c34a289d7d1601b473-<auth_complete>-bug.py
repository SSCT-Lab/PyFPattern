

def auth_complete(self, *args, **kwargs):
    'Completes loging process, must return user instance'
    self.process_error(self.data)
    params = self.auth_complete_params(self.validate_state())
    try:
        response = requests.post(self.ACCESS_TOKEN_URL, data=params, headers=self.auth_headers())
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if (e.code == 400):
            raise AuthCanceled(self)
        else:
            raise
    else:
        try:
            response = response.json()
        except (ValueError, KeyError):
            raise AuthUnknownError(self)
    response.pop('data')
    self.process_error(response)
    return self.do_auth(response['access_token'], *args, response=response, **kwargs)
