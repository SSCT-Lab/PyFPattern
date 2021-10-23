def _read_user_execute(self):
    '\n        Returns the command line for reading a crontab\n        '
    user = ''
    if self.user:
        if (platform.system() == 'SunOS'):
            return ("su %s -c '%s -l'" % (pipes.quote(self.user), pipes.quote(CRONCMD)))
        elif (platform.system() == 'AIX'):
            return ('%s -l %s' % (pipes.quote(CRONCMD), pipes.quote(self.user)))
        elif (platform.system() == 'HP-UX'):
            return ('%s %s %s' % (CRONCMD, '-l', pipes.quote(self.user)))
        elif (pwd.getpwuid(os.getuid())[0] != self.user):
            user = ('-u %s' % pipes.quote(self.user))
    return ('%s %s %s' % (CRONCMD, user, '-l'))