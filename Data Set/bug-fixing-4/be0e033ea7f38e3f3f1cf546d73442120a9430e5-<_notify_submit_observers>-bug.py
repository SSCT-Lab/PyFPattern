def _notify_submit_observers(self):
    for (cid, func) in self.submit_observers.items():
        func(self.text)