

def parse_stacks(self, data):
    match = re.findall('^Model [Nn]umber\\s+: (\\S+)', data, re.M)
    if match:
        self.facts['stacked_models'] = match
    match = re.findall('^System [Ss]erial [Nn]umber\\s+: (\\S+)', data, re.M)
    if match:
        self.facts['stacked_serialnums'] = match
