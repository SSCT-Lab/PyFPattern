def instrumented_task(name, stat_suffix=None, **kwargs):

    def wrapped(func):

        @wraps(func)
        def _wrapped(*args, **kwargs):
            transaction_id = kwargs.pop('__transaction_id', None)
            key = 'jobs.duration'
            if stat_suffix:
                instance = '{}.{}'.format(name, stat_suffix(*args, **kwargs))
            else:
                instance = name
            with configure_scope() as scope:
                scope.set_tag('task_name', name)
                scope.set_tag('transaction_id', transaction_id)
            with metrics.timer(key, instance=instance), track_memory_usage('jobs.memory_change', instance=instance):
                result = func(*args, **kwargs)
            return result
        return app.task(name=name, **kwargs)(_wrapped)
    return wrapped