def v2_playbook_on_task_start(self, task, is_conditional):
    self.last_task = task
    self.shown_title = False