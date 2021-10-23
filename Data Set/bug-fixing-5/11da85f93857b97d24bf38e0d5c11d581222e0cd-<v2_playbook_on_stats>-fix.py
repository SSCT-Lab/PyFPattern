def v2_playbook_on_stats(self, stats):
    end_time = datetime.utcnow()
    runtime = (end_time - self.start_time)
    self._display.display(('Playbook run took %s days, %s hours, %s minutes, %s seconds' % self.days_hours_minutes_seconds(runtime)))