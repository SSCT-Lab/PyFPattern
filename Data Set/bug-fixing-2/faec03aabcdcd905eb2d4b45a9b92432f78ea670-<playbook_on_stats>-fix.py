

def playbook_on_stats(self, stats):
    self._display.display(tasktime())
    self._display.display(filled('', fchar='='))
    timestamp(self)
    results = self.stats.items()
    if (self.sort_order != 'none'):
        results = sorted(self.stats.iteritems(), key=(lambda x: x[1]['time']), reverse=self.sort_order)
    results = results[:self.task_output_limit]
    for (uuid, result) in results:
        msg = '{0:-<70} {1:->9}'.format(result['name'], ' {0:.02f}s'.format(result['time']))
        if ('path' in result):
            msg += '\n{0:-<79}'.format(result['path'])
        self._display.display(msg)
