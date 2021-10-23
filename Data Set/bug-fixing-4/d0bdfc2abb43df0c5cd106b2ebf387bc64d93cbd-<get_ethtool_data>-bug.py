def get_ethtool_data(self, device):
    features = {
        
    }
    ethtool_path = self.module.get_bin_path('ethtool')
    if ethtool_path:
        args = [ethtool_path, '-k', device]
        (rc, stdout, stderr) = self.module.run_command(args)
        stdout = stdout.decode('utf-8', 'replace')
        if (rc == 0):
            for line in stdout.strip().split('\n'):
                if ((not line) or line.endswith(':')):
                    continue
                (key, value) = line.split(': ')
                if (not value):
                    continue
                features[key.strip().replace('-', '_')] = value.strip()
    return features