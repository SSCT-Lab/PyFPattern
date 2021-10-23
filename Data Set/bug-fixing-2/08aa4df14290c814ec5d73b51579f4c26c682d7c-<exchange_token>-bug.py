

def exchange_token(self, request, pipeline, code):
    data = self.get_token_params(code=code, redirect_uri=absolute_uri(pipeline.redirect_url()))
    verify_ssl = pipeline.config.get('verify_ssl', True)
    req = safe_urlopen(self.access_token_url, data=data, verify_ssl=verify_ssl)
    body = safe_urlread(req)
    if req.headers['Content-Type'].startswith('application/x-www-form-urlencoded'):
        return dict(parse_qsl(body))
    return json.loads(body)
