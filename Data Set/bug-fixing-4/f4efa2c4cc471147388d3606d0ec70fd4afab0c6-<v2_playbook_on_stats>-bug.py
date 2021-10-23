def v2_playbook_on_stats(self, stats):
    self._display.banner('PLAY RECAP')
    hosts = sorted(stats.processed.keys())
    for h in hosts:
        t = stats.summarize(h)
        self._display.display(('%s : %s %s %s %s' % (hostcolor(h, t), colorize('ok', t['ok'], C.COLOR_OK), colorize('changed', t['changed'], C.COLOR_CHANGED), colorize('unreachable', t['unreachable'], C.COLOR_UNREACHABLE), colorize('failed', t['failures'], C.COLOR_ERROR))), screen_only=True)
        self._display.display(('%s : %s %s %s %s' % (hostcolor(h, t, False), colorize('ok', t['ok'], None), colorize('changed', t['changed'], None), colorize('unreachable', t['unreachable'], None), colorize('failed', t['failures'], None))), log_only=True)
    self._display.display('', screen_only=True)
    if (self._plugin_options.get('show_custom_stats', C.SHOW_CUSTOM_STATS) and stats.custom):
        self._display.banner('CUSTOM STATS: ')
        for k in sorted(stats.custom.keys()):
            if (k == '_run'):
                continue
            self._display.display(('\t%s: %s' % (k, self._dump_results(stats.custom[k], indent=1).replace('\n', ''))))
        if ('_run' in stats.custom):
            self._display.display('', screen_only=True)
            self._display.display(('\tRUN: %s' % self._dump_results(stats.custom['_run'], indent=1).replace('\n', '')))
        self._display.display('', screen_only=True)