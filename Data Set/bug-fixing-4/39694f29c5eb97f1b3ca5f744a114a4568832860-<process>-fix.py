def process(self, s, *args, **kwargs):
    '\n        Process signal *s*.\n\n        All of the functions registered to receive callbacks on *s* will be\n        called with ``*args`` and ``**kwargs``.\n        '
    if (s in self.callbacks):
        for (cid, proxy) in list(six.iteritems(self.callbacks[s])):
            try:
                proxy(*args, **kwargs)
            except ReferenceError:
                self._remove_proxy(proxy)
            except Exception as exc:
                if (self.exception_handler is not None):
                    self.exception_handler(exc)
                else:
                    raise