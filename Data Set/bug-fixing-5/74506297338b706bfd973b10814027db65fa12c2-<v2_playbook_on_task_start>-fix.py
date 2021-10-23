def v2_playbook_on_task_start(self, task, is_conditional):
    if (self._play.strategy != 'free'):
        self._print_task_banner(task)