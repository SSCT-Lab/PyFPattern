def run(self):
    if self.running:
        return
    next_run = (time.time() + (self.interval * random.random()))
    while self.running:
        started = time.time()
        if (next_run >= started):
            try:
                self.callback()
            except Exception:
                logging.error('bgtask.failed', exc_info=True, extra=dict(task_name=self.name))
            next_run = (started + self.interval)
        time.sleep(1.0)