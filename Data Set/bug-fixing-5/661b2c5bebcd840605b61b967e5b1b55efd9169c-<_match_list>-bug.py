def _match_list(self, items, item_attr, pattern_str):
    results = []
    try:
        if (not pattern_str.startswith('~')):
            pattern = re.compile(fnmatch.translate(pattern_str))
        else:
            pattern = re.compile(pattern_str[1:])
    except Exception:
        raise AnsibleError(('invalid host list pattern: %s' % pattern_str))
    for item in items:
        if pattern.match(getattr(item, item_attr)):
            results.append(item)
    return results