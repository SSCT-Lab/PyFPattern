def run(self):
    if self.running:
        return
    self.running = True
    next_run = (time.time() + (self.interval * random.random()))
    while self.running:
        now = time.time()
        if (now >= next_run):
            try:
                self.callback()
            except Exception:
                logging.error('bgtask.failed', exc_info=True, extra=dict(task_name=self.name))
            next_run = (now + self.interval)
        time.sleep(1.0)