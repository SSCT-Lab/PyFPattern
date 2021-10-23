def parse_distribution_file_NA(self, name, data, path, collected_facts):
    na_facts = {
        
    }
    for line in data.splitlines():
        distribution = re.search('^NAME=(.*)', line)
        if (distribution and (collected_facts['distribution'] == 'NA')):
            na_facts['distribution'] = distribution.group(1).strip('"')
        version = re.search('^VERSION=(.*)', line)
        if (version and (collected_facts['distribution_version'] == 'NA')):
            na_facts['distribution_version'] = version.group(1).strip('"')
    return (True, na_facts)