def v2_playbook_on_stats(self, stats):
    summarize_stat = {
        
    }
    for host in stats.processed.keys():
        summarize_stat[host] = stats.summarize(host)
    if (self.errors == 0):
        status = 'OK'
    else:
        status = 'FAILED'
    data = {
        'status': status,
        'host': self.hostname,
        'session': self.session,
        'ansible_type': 'finish',
        'ansible_playbook': self.playbook,
        'ansible_result': json.dumps(summarize_stat),
    }
    self.logger.info('ansible stats', extra=data)