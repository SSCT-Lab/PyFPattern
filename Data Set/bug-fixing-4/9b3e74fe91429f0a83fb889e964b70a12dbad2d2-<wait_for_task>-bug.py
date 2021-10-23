@staticmethod
def wait_for_task(task):
    while (task.info.state not in ['error', 'success']):
        time.sleep(1)