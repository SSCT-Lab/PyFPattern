

def update_local(self):
    'Update CPU stats using PSUtil.'
    self.stats['total'] = cpu_percent.get()
    cpu_times_percent = psutil.cpu_times_percent(interval=0.0)
    for stat in ['user', 'system', 'idle', 'nice', 'iowait', 'irq', 'softirq', 'steal', 'guest', 'guest_nice']:
        if hasattr(cpu_times_percent, stat):
            self.stats[stat] = getattr(cpu_times_percent, stat)
    try:
        cpu_stats = psutil.cpu_stats()
    except AttributeError:
        pass
    else:
        time_since_update = getTimeSinceLastUpdate('cpu')
        if (not hasattr(self, 'cpu_stats_old')):
            self.cpu_stats_old = cpu_stats
        else:
            for stat in cpu_stats._fields:
                self.stats[stat] = (getattr(cpu_stats, stat) - getattr(self.cpu_stats_old, stat))
            self.stats['time_since_update'] = time_since_update
            self.stats['cpucore'] = self.nb_log_core
            self.cpu_stats_old = cpu_stats
