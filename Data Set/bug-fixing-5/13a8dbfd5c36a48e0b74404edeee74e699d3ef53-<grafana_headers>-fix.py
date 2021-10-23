def grafana_headers(self):
    headers = {
        'content-type': 'application/json; charset=utf8',
    }
    if self.grafana_api_key:
        headers['Authorization'] = ('Bearer %s==' % self.grafana_api_key)
    else:
        headers['Authorization'] = basic_auth_header(self.grafana_user, self.grafana_password)
        self.grafana_switch_organisation(headers)
    return headers