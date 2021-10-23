

def set_options(self, task_keys=None, var_options=None, direct=None):
    super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
    self.grafana_api_key = self.get_option('grafana_api_key')
    self.grafana_url = self.get_option('grafana_url')
    self.validate_grafana_certs = self.get_option('validate_certs')
    self.http_agent = self.get_option('http_agent')
    self.grafana_user = self.get_option('grafana_user')
    self.grafana_password = self.get_option('grafana_password')
    self.dashboard_id = self.get_option('grafana_dashboard_id')
    self.panel_id = self.get_option('grafana_panel_id')
    if self.grafana_api_key:
        self.headers['Authorization'] = ('Bearer %s' % self.grafana_api_key)
    else:
        self.force_basic_auth = True
    if (self.grafana_url is None):
        self.disabled = True
        self._display.warning('Grafana URL was not provided. The Grafana URL can be provided using the `GRAFANA_URL` environment variable.')
    self._display.info(('Grafana URL: %s' % self.grafana_url))
