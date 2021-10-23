def _write_execute(self, path):
    '\n        Return the command line for writing a crontab\n        '
    user = ''
    if self.user:
        if (platform.system() in ['SunOS', 'HP-UX', 'AIX']):
            return ("chown %s %s ; su '%s' -c '%s %s'" % (pipes.quote(self.user), pipes.quote(path), pipes.quote(self.user), CRONCMD, pipes.quote(path)))
        elif (pwd.getpwuid(os.getuid())[0] != self.user):
            user = ('-u %s' % pipes.quote(self.user))
    return ('%s %s %s' % (CRONCMD, user, pipes.quote(path)))