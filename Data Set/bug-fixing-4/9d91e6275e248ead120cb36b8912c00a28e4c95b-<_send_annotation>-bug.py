def _send_annotation(self, annotation):
    try:
        response = open_url(self.grafana_url, data=annotation, headers=self.headers, method='POST', validate_certs=self.validate_grafana_certs, url_username=self.grafana_user, url_password=self.grafana_password, http_agent=self.http_agent, force_basic_auth=self.force_basic_auth)
    except Exception as e:
        self._display.error(('Could not submit message to Grafana: %s' % to_text(e)))