def parse_model(self, data):
    match = re.findall('^Model number\\s+: (\\S+)', data, re.M)
    if match:
        return match
    else:
        match = re.search('^[Cc]isco (\\S+).+bytes of memory', data, re.M)
        if match:
            return [match.group(1)]