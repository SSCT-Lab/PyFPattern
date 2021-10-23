def _notify_change_observers(self):
    if self.eventson:
        for (cid, func) in self.change_observers.items():
            func(self.text)