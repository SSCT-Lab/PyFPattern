

def get_distribution_FreeBSD(self):
    freebsd_facts = {
        
    }
    freebsd_facts['distribution_release'] = platform.release()
    data = re.search('(\\d+)\\.(\\d+)-(RELEASE|STABLE).*', freebsd_facts['distribution_release'])
    if data:
        freebsd_facts['distribution_major_version'] = data.group(1)
        freebsd_facts['distribution_version'] = ('%s.%s' % (data.group(1), data.group(2)))
    return freebsd_facts
