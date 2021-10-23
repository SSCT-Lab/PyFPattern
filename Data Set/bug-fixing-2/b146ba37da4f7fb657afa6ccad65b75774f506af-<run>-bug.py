

def run(self):
    current = self.getcap(self.path)
    caps = [cap[0] for cap in current]
    if ((self.state == 'present') and (self.capability_tup not in current)):
        if self.module.check_mode:
            self.module.exit_json(changed=True, msg='capabilities changed')
        else:
            current = filter((lambda x: (x[0] != self.capability_tup[0])), current)
            current.append(self.capability_tup)
            self.module.exit_json(changed=True, state=self.state, msg='capabilities changed', stdout=self.setcap(self.path, current))
    elif ((self.state == 'absent') and (self.capability_tup[0] in caps)):
        if self.module.check_mode:
            self.module.exit_json(changed=True, msg='capabilities changed')
        else:
            current = filter((lambda x: (x[0] != self.capability_tup[0])), current)
            self.module.exit_json(changed=True, state=self.state, msg='capabilities changed', stdout=self.setcap(self.path, current))
    self.module.exit_json(changed=False, state=self.state)
