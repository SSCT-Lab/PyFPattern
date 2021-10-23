def v2_playbook_on_stats(self, stats):
    'Display info about playbook statistics'
    hosts = sorted(stats.processed.keys())
    summary = {
        
    }
    for h in hosts:
        s = stats.summarize(h)
        summary[h] = s
    output = {
        'plays': self.results,
        'stats': summary,
    }
    self._display.display(json.dumps(output, indent=4, sort_keys=True))