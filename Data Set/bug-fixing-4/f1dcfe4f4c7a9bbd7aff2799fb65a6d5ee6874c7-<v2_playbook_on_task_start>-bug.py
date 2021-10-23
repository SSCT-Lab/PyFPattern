def v2_playbook_on_task_start(self, task, is_conditional):
    if (self._play.strategy != 'free'):
        self._last_task_name = task.get_name().strip()
        if (self._plugin_options.get('display_skipped_hosts', DEFAULT_DISPLAY_SKIPPED_HOSTS) and self._plugin_options.get('display_ok_hosts', DEFAULT_DISPLAY_OK_HOSTS)):
            self._print_task_banner(task)