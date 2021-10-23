def capture_signal(type):

    def wrapped(instance, **kwargs):
        analytics.record(type, instance)
    return wrapped