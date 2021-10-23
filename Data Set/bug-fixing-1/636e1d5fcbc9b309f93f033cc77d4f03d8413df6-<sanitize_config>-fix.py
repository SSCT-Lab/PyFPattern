

def sanitize_config(config, result):
    result['filtered'] = list()
    for regex in CONFIG_FILTERS:
        for (index, line) in reversed(list(enumerate(config))):
            if regex.search(line):
                result['filtered'].append(line)
                del config[index]
