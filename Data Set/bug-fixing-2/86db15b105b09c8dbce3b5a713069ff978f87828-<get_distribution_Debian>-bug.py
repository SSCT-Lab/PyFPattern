

def get_distribution_Debian(self, name, data, path):
    if (('Debian' in data) or ('Raspbian' in data)):
        self.facts['distribution'] = 'Debian'
        release = re.search('PRETTY_NAME=[^(]+ \\(?([^)]+?)\\)', data)
        if release:
            self.facts['distribution_release'] = release.groups()[0]
    elif ('Ubuntu' in data):
        self.facts['distribution'] = 'Ubuntu'
        pass
    else:
        return False
