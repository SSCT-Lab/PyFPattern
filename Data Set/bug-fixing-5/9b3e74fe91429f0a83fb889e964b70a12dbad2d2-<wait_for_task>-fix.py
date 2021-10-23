def wait_for_task(self, task, poll_interval=1):
    "\n        Wait for a VMware task to complete.  Terminal states are 'error' and 'success'.\n\n        Inputs:\n          - task: the task to wait for\n          - poll_interval: polling interval to check the task, in seconds\n\n        Modifies:\n          - self.change_applied\n        "
    while (task.info.state not in ['error', 'success']):
        time.sleep(poll_interval)
    self.change_applied = (self.change_applied or (task.info.state == 'success'))