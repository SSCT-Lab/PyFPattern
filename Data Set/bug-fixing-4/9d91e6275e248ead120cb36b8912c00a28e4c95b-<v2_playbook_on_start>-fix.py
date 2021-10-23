def v2_playbook_on_start(self, playbook):
    self.playbook = playbook._file_name
    text = PLAYBOOK_START_TXT.format(playbook=self.playbook, hostname=self.hostname, username=self.username)
    data = {
        'time': to_millis(self.start_time),
        'text': text,
        'tags': ['ansible', 'ansible_event_start', self.playbook],
    }
    self._send_annotation(data)