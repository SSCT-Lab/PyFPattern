def _new_task(self, task):
    return {
        'task': {
            'name': task.name,
            'id': str(task._uuid),
        },
        'hosts': {
            
        },
    }