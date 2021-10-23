

def connect(self, receiver, sender=None, weak=True, dispatch_uid=None):
    '\n        Connect receiver to sender for signal.\n\n        Arguments:\n\n            receiver\n                A function or an instance method which is to receive signals.\n                Receivers must be hashable objects.\n\n                If weak is True, then receiver must be weak referenceable.\n\n                Receivers must be able to accept keyword arguments.\n\n                If a receiver is connected with a dispatch_uid argument, it\n                will not be added if another receiver was already connected\n                with that dispatch_uid.\n\n            sender\n                The sender to which the receiver should respond. Must either be\n                a Python object, or None to receive events from any sender.\n\n            weak\n                Whether to use weak references to the receiver. By default, the\n                module will attempt to use weak references to the receiver\n                objects. If this parameter is false, then strong references will\n                be used.\n\n            dispatch_uid\n                An identifier used to uniquely identify a particular instance of\n                a receiver. This will usually be a string, though it may be\n                anything hashable.\n        '
    from django.conf import settings
    if (settings.configured and settings.DEBUG):
        assert callable(receiver), 'Signal receivers must be callable.'
        if (not func_accepts_kwargs(receiver)):
            raise ValueError('Signal receivers must accept keyword arguments (**kwargs).')
    if dispatch_uid:
        lookup_key = (dispatch_uid, _make_id(sender))
    else:
        lookup_key = (_make_id(receiver), _make_id(sender))
    if weak:
        ref = weakref.ref
        receiver_object = receiver
        if (hasattr(receiver, '__self__') and hasattr(receiver, '__func__')):
            ref = WeakMethod
            receiver_object = receiver.__self__
        if six.PY3:
            receiver = ref(receiver)
            weakref.finalize(receiver_object, self._remove_receiver)
        else:
            receiver = ref(receiver, self._remove_receiver)
    with self.lock:
        self._clear_dead_receivers()
        for (r_key, _) in self.receivers:
            if (r_key == lookup_key):
                break
        else:
            self.receivers.append((lookup_key, receiver))
        self.sender_receivers_cache.clear()
