def get_distribution_Debian(self, name, data, path):
    if (('Debian' in data) or ('Raspbian' in data)):
        self.facts['distribution'] = 'Debian'
        release = re.search('PRETTY_NAME=[^(]+ \\(?([^)]+?)\\)', data)
        if release:
            self.facts['distribution_release'] = release.groups()[0]
        if ((self.facts['distribution_release'] == 'NA') and ('Debian' in data)):
            dpkg_cmd = self.module.get_bin_path('dpkg')
            if dpkg_cmd:
                cmd = ("%s --status tzdata|grep Provides|cut -f2 -d'-'" % dpkg_cmd)
                (rc, out, err) = self.module.run_command(cmd)
                if (rc == 0):
                    self.facts['distribution_release'] = out.strip()
    elif ('Ubuntu' in data):
        self.facts['distribution'] = 'Ubuntu'