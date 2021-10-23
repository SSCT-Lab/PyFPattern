

def svcadm_supports_sync(self):
    for line in open('/etc/release', 'r').readlines():
        m = re.match('\\s+Oracle Solaris (\\d+\\.\\d+).*', line.rstrip())
        if (m and (m.groups()[0] > 10)):
            return True
