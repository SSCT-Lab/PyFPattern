def capture_signal(type):

    def wrapped(instance, created, **kwargs):
        if created:
            analytics.record(type, instance)
    return wrapped