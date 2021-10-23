@classmethod
def to_python(cls, data):
    threads = []
    for thread in (data.get('values') or ()):
        stacktrace = thread.get('stacktrace')
        if (stacktrace is not None):
            stacktrace = Stacktrace.to_python(stacktrace, slim_frames=True)
        threads.append({
            'stacktrace': stacktrace,
            'id': trim(thread.get('id'), 40),
            'crashed': bool(thread.get('crashed')),
            'current': bool(thread.get('current')),
            'name': trim(thread.get('name'), 200),
        })
    return cls(values=threads)