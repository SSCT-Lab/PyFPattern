

def get_cron_job(self, minute, hour, day, month, weekday, job, special, disabled):
    job = job.strip('\r\n')
    if disabled:
        disable_prefix = '#'
    else:
        disable_prefix = ''
    if special:
        if self.cron_file:
            return ('%s@%s %s %s' % (disable_prefix, special, self.user, job))
        else:
            return ('%s@%s %s' % (disable_prefix, special, job))
    elif self.cron_file:
        return ('%s%s %s %s %s %s %s %s' % (disable_prefix, minute, hour, day, month, weekday, self.user, job))
    else:
        return ('%s%s %s %s %s %s %s' % (disable_prefix, minute, hour, day, month, weekday, job))
