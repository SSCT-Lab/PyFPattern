def v2_playbook_on_task_start(self, task, is_conditional):
    self.last_task = task
    self.last_task_banner = self._get_task_banner(task)
    self.shown_title = False