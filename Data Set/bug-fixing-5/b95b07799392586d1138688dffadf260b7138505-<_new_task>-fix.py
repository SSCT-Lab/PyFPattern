def _new_task(self, task):
    return {
        'task': {
            'name': task.get_name(),
            'id': str(task._uuid),
        },
        'hosts': {
            
        },
    }