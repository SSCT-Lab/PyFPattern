def get_lsb_facts(self):
    lsb_path = self.module.get_bin_path('lsb_release')
    if lsb_path:
        (rc, out, err) = self.module.run_command([lsb_path, '-a'])
        if (rc == 0):
            out = out.decode('utf-8', 'replace')
            self.facts['lsb'] = {
                
            }
            for line in out.split('\n'):
                if ((len(line) < 1) or (':' not in line)):
                    continue
                value = line.split(':', 1)[1].strip()
                if ('LSB Version:' in line):
                    self.facts['lsb']['release'] = value
                elif ('Distributor ID:' in line):
                    self.facts['lsb']['id'] = value
                elif ('Description:' in line):
                    self.facts['lsb']['description'] = value
                elif ('Release:' in line):
                    self.facts['lsb']['release'] = value
                elif ('Codename:' in line):
                    self.facts['lsb']['codename'] = value
    elif ((lsb_path is None) and os.path.exists('/etc/lsb-release')):
        self.facts['lsb'] = {
            
        }
        for line in get_file_lines('/etc/lsb-release'):
            value = line.split('=', 1)[1].strip()
            if ('DISTRIB_ID' in line):
                self.facts['lsb']['id'] = value
            elif ('DISTRIB_RELEASE' in line):
                self.facts['lsb']['release'] = value
            elif ('DISTRIB_DESCRIPTION' in line):
                self.facts['lsb']['description'] = value
            elif ('DISTRIB_CODENAME' in line):
                self.facts['lsb']['codename'] = value
    if (('lsb' in self.facts) and ('release' in self.facts['lsb'])):
        self.facts['lsb']['major_release'] = self.facts['lsb']['release'].split('.')[0]