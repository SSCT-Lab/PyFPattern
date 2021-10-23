def v2_playbook_on_stats(self, stats):
    end_time = datetime.now()
    duration = (end_time - self.start_time)
    summarize_stat = {
        
    }
    for host in stats.processed.keys():
        summarize_stat[host] = stats.summarize(host)
    status = 'FAILED'
    if (self.errors == 0):
        status = 'OK'
    text = PLAYBOOK_STATS_TXT.format(playbook=self.playbook, hostname=self.hostname, duration=duration.total_seconds(), status=status, username=self.username, summary=json.dumps(summarize_stat))
    data = {
        'time': to_millis(self.start_time),
        'timeEnd': to_millis(end_time),
        'isRegion': True,
        'text': text,
        'tags': ['ansible', 'ansible_report', self.playbook],
    }
    if self.dashboard_id:
        data['dashboardId'] = int(self.dashboard_id)
    if self.panel_id:
        data['panelId'] = int(self.panel_id)
    self._send_annotation(json.dumps(data))