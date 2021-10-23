def _notify_change_observers(self):
    for (cid, func) in self.change_observers.items():
        func(self.text)