def install_monitor(self, mon):
    'Installs monitor on all executors '
    assert self.binded
    self._monitor = mon
    for mod in self._buckets.values():
        mod.install_monitor(mon)