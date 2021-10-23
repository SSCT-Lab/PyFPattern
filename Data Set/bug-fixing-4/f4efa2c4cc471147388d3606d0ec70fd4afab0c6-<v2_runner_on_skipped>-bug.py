def v2_runner_on_skipped(self, result):
    if self._plugin_options.get('display_skipped_hosts', C.DISPLAY_SKIPPED_HOSTS):
        self._clean_results(result._result, result._task.action)
        if (self._last_task_banner != result._task._uuid):
            self._print_task_banner(result._task)
        if (result._task.loop and ('results' in result._result)):
            self._process_items(result)
        else:
            msg = ('skipping: [%s]' % result._host.get_name())
            if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and ('_ansible_verbose_override' not in result._result)):
                msg += (' => %s' % self._dump_results(result._result))
            self._display.display(msg, color=C.COLOR_SKIP)