def grafana_headers(self):
    headers = {
        'content-type': 'application/json; charset=utf8',
    }
    if self.grafana_api_key:
        headers['Authorization'] = ('Bearer %s==' % self.grafana_api_key)
    else:
        auth = base64.b64encode(to_bytes(('%s:%s' % (self.grafana_user, self.grafana_password))).replace('\n', ''))
        headers['Authorization'] = ('Basic %s' % auth)
        self.grafana_switch_organisation(headers)
    return headers