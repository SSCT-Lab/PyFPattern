def v2_playbook_on_stats(self, stats):
    'Display info about playbook statistics'
    hosts = sorted(stats.processed.keys())
    summary = {
        
    }
    for h in hosts:
        s = stats.summarize(h)
        summary[h] = s
    custom_stats = {
        
    }
    if (self.get_option('show_custom_stats') and stats.custom):
        custom_stats.update(dict(((self._convert_host_to_name(k), v) for (k, v) in stats.custom.items())))
        custom_stats.pop('_run', None)
    output = {
        'plays': self.results,
        'stats': summary,
        'custom_stats': custom_stats,
    }
    self._display.display(json.dumps(output, indent=4, sort_keys=True))