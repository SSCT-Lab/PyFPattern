def connect(self, s, func):
    '\n        register *func* to be called when a signal *s* is generated\n        func will be called\n        '
    self._func_cid_map.setdefault(s, WeakKeyDictionary())
    proxy = _BoundMethodProxy(func)
    if (proxy in self._func_cid_map[s]):
        return self._func_cid_map[s][proxy]
    proxy.add_destroy_callback(self._remove_proxy)
    self._cid += 1
    cid = self._cid
    self._func_cid_map[s][proxy] = cid
    self.callbacks.setdefault(s, dict())
    self.callbacks[s][cid] = proxy
    return cid