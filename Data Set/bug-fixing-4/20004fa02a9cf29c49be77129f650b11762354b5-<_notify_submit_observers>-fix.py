def _notify_submit_observers(self):
    if self.eventson:
        for (cid, func) in self.submit_observers.items():
            func(self.text)