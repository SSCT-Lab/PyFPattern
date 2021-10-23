def v2_playbook_on_stats(self, stats):
    'Display info about playbook statistics.'
    print()
    self.printed_last_task = False
    self._print_task('STATS')
    hosts = sorted(stats.processed.keys())
    for host in hosts:
        s = stats.summarize(host)
        if (s['failures'] or s['unreachable']):
            color = 'failed'
        elif s['changed']:
            color = 'changed'
        else:
            color = 'ok'
        msg = '{}    : ok={}\tchanged={}\tfailed={}\tunreachable={}'.format(host, s['ok'], s['changed'], s['failures'], s['unreachable'])
        print(colorize(msg, color))