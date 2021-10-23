def install_monitor(self, mon):
    'Installs monitor on all executors '
    assert self.binded
    for mod in self._buckets.values():
        mod.install_monitor(mon)