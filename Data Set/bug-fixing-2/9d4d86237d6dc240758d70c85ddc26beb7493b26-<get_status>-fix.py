

def get_status(self):
    (rc, out, err) = self.execute_command([self.svstat_cmd, 'status', self.svc_full])
    if ((err is not None) and err):
        self.full_state = self.state = err
    else:
        self.full_state = out
        full_state_no_logger = self.full_state.split('; ')[0]
        m = re.search('\\(pid (\\d+)\\)', full_state_no_logger)
        if m:
            self.pid = m.group(1)
        m = re.search(' (\\d+)s', full_state_no_logger)
        if m:
            self.duration = m.group(1)
        if re.search('^run:', full_state_no_logger):
            self.state = 'started'
        elif re.search('^down:', full_state_no_logger):
            self.state = 'stopped'
        else:
            self.state = 'unknown'
            return
