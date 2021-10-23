

def get_status(self):
    (rc, out, err) = self.execute_command([self.svstat_cmd, 'status', self.svc_full])
    if ((err is not None) and err):
        self.full_state = self.state = err
    else:
        self.full_state = out
        m = re.search('\\(pid (\\d+)\\)', out)
        if m:
            self.pid = m.group(1)
        m = re.search(' (\\d+)s', out)
        if m:
            self.duration = m.group(1)
        if re.search('run:', out):
            self.state = 'started'
        elif re.search('down:', out):
            self.state = 'stopped'
        else:
            self.state = 'unknown'
            return
