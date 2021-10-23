def _match_list(self, items, pattern_str):
    try:
        if (not pattern_str.startswith('~')):
            pattern = re.compile(fnmatch.translate(pattern_str))
        else:
            pattern = re.compile(pattern_str[1:])
    except Exception:
        raise AnsibleError(('Invalid host list pattern: %s' % pattern_str))
    results = []
    for item in items:
        if pattern.match(item):
            results.append(item)
    return results