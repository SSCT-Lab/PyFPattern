def get_password_defaults(self):
    try:
        minweeks = ''
        maxweeks = ''
        warnweeks = ''
        for line in open('/etc/default/passwd', 'r'):
            line = line.strip()
            if (line.startswith('#') or (line == '')):
                continue
            (key, value) = line.split('=')
            if (key == 'MINWEEKS'):
                minweeks = value.rstrip('\n')
            elif (key == 'MAXWEEKS'):
                maxweeks = value.rstrip('\n')
            elif (key == 'WARNWEEKS'):
                warnweeks = value.rstrip('\n')
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('failed to read /etc/default/passwd: %s' % str(err)))
    return (minweeks, maxweeks, warnweeks)