

def get_status(self):
    (rc, out, err) = self.execute_command([self.svstat_cmd, self.svc_full])
    if ((err is not None) and err):
        self.full_state = self.state = err
    else:
        self.full_state = out
        m = re.search('\\(pid (\\d+)\\)', out)
        if m:
            self.pid = m.group(1)
        m = re.search('(\\d+) seconds', out)
        if m:
            self.duration = m.group(1)
        if re.search(' up ', out):
            self.state = 'start'
        elif re.search(' down ', out):
            self.state = 'stopp'
        else:
            self.state = 'unknown'
            return
        if re.search(' want ', out):
            self.state += 'ing'
        else:
            self.state += 'ed'
