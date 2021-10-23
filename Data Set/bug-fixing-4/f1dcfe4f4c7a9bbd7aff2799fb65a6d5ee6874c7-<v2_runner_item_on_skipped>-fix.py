def v2_runner_item_on_skipped(self, result):
    if self.display_skipped_hosts:
        self._clean_results(result._result, result._task.action)
        msg = ('skipping: [%s] => (item=%s) ' % (result._host.get_name(), self._get_item_label(result._result)))
        if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and ('_ansible_verbose_override' not in result._result)):
            msg += (' => %s' % self._dump_results(result._result))
        self._display.display(msg, color=C.COLOR_SKIP)