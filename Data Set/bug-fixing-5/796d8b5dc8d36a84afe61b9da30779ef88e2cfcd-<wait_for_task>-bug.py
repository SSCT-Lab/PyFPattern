def wait_for_task(task, max_backoff=64, timeout=3600):
    'Wait for given task using exponential back-off algorithm.\n\n    Args:\n        task: VMware task object\n        max_backoff: Maximum amount of sleep time in seconds\n        timeout: Timeout for the given task in seconds\n\n    Returns: Tuple with True and result for successful task\n    Raises: TaskError on failure\n    '
    failure_counter = 0
    start_time = time.time()
    while True:
        if ((time.time() - start_time) >= timeout):
            raise TaskError('Timeout')
        if (task.info.state == vim.TaskInfo.State.success):
            return (True, task.info.result)
        if (task.info.state == vim.TaskInfo.State.error):
            error_msg = task.info.error
            try:
                error_msg = error_msg.msg
            except AttributeError:
                pass
            finally:
                raise_from(TaskError(error_msg), task.info.error)
        if (task.info.state in [vim.TaskInfo.State.running, vim.TaskInfo.State.queued]):
            sleep_time = min(((2 ** failure_counter) + randint(1, 1000)), max_backoff)
            time.sleep(sleep_time)
            failure_counter += 1