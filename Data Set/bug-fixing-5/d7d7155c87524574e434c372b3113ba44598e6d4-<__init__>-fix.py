def __init__(self, *args, **kwargs):
    StacktraceProcessor.__init__(self, *args, **kwargs)
    self.use_symbolicator = _is_symbolicator_enabled(self.project, self.data)
    metrics.incr('native.use_symbolicator', tags={
        'value': self.use_symbolicator,
    })
    self.arch = cpu_name_from_data(self.data)
    self.signal = signal_from_data(self.data)
    self.sym = None
    self.difs_referenced = set()
    images = get_path(self.data, 'debug_meta', 'images', default=(), filter=self._is_valid_image)
    if images:
        self.available = True
        self.sdk_info = get_sdk_from_event(self.data)
        self.object_lookup = ObjectLookup(images)
        self.images = images
    else:
        self.available = False