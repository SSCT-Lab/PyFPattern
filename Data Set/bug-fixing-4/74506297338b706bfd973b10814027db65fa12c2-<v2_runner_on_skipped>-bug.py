def v2_runner_on_skipped(self, result):
    if C.DISPLAY_SKIPPED_HOSTS:
        if (result._task.loop and ('results' in result._result)):
            self._process_items(result)
        else:
            msg = ('skipping: [%s]' % result._host.get_name())
            if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and (not ('_ansible_verbose_override' in result._result))):
                msg += (' => %s' % self._dump_results(result._result))
            self._display.display(msg, color=C.COLOR_SKIP)