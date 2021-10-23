def v2_runner_on_failed(self, result, **kwargs):
    text = PLAYBOOK_ERROR_TXT.format(playbook=self.playbook, hostname=self.hostname, username=self.username, task=result._task, host=result._host.name, result=self._dump_results(result._result))
    data = {
        'time': to_millis(datetime.now()),
        'text': text,
        'tags': ['ansible', 'ansible_event_failure', self.playbook],
    }
    self.errors += 1
    self._send_annotations(data)