def v2_playbook_on_start(self, playbook):
    self.playbook = playbook._file_name
    text = PLAYBOOK_START_TXT.format(playbook=self.playbook, hostname=self.hostname, username=self.username)
    data = {
        'time': to_millis(self.start_time),
        'text': text,
        'tags': ['ansible', 'ansible_event_start', self.playbook],
    }
    if self.dashboard_id:
        data['dashboardId'] = int(self.dashboard_id)
    if self.panel_id:
        data['panelId'] = int(self.panel_id)
    self._send_annotation(json.dumps(data))