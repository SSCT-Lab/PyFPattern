def get_caps_facts(self):
    capsh_path = self.module.get_bin_path('capsh')
    if capsh_path:
        (rc, out, err) = self.module.run_command([capsh_path, '--print'], errors='surrogate_or_replace')
        enforced_caps = []
        enforced = 'NA'
        for line in out.split('\n'):
            if (len(line) < 1):
                continue
            if line.startswith('Current:'):
                if (line.split(':')[1].strip() == '=ep'):
                    enforced = 'False'
                else:
                    enforced = 'True'
                    enforced_caps = [i.strip() for i in line.split('=')[1].split(',')]
        self.facts['system_capabilities_enforced'] = enforced
        self.facts['system_capabilities'] = enforced_caps