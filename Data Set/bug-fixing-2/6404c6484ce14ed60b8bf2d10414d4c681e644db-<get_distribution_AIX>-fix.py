

def get_distribution_AIX(self):
    aix_facts = {
        
    }
    (rc, out, err) = self.module.run_command('/usr/bin/oslevel')
    data = out.split('.')
    aix_facts['distribution_major_version'] = data[0]
    if (len(data) > 1):
        aix_facts['distribution_version'] = ('%s.%s' % (data[0], data[1]))
        aix_facts['distribution_release'] = data[1]
    else:
        aix_facts['distribution_version'] = data[0]
    return aix_facts
