

def get_distribution_AIX(self):
    aix_facts = {
        
    }
    (rc, out, err) = self.module.run_command('/usr/bin/oslevel')
    data = out.split('.')
    aix_facts['distribution_version'] = data[0]
    aix_facts['distribution_release'] = data[1]
    return aix_facts
