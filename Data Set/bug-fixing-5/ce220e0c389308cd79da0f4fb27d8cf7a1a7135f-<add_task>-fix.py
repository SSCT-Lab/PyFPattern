def add_task(self, task):
    '\n        Add a task to the DAG\n\n        :param task: the task you want to add\n        :type task: task\n        '
    if ((not self.start_date) and (not task.start_date)):
        raise AirflowException('Task is missing the start_date parameter')
    if (not task.start_date):
        task.start_date = self.start_date
    if (task.task_id in self.task_dict):
        raise AirflowException("Task id '{0}' has already been added to the DAG ".format(task.task_id))
    else:
        self.tasks.append(task)
        self.task_dict[task.task_id] = task
        task.dag = self
    self.task_count = len(self.tasks)