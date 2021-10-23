def v2_runner_on_failed(self, result, **kwargs):
    text = PLAYBOOK_ERROR_TXT.format(playbook=self.playbook, hostname=self.hostname, username=self.username, task=result._task, host=result._host.name, result=self._dump_results(result._result))
    data = {
        'time': to_millis(datetime.now()),
        'text': text,
        'tags': ['ansible', 'ansible_event_failure', self.playbook],
    }
    self.errors += 1
    if self.dashboard_id:
        data['dashboardId'] = int(self.dashboard_id)
    if self.panel_id:
        data['panelId'] = int(self.panel_id)
    self._send_annotation(json.dumps(data))