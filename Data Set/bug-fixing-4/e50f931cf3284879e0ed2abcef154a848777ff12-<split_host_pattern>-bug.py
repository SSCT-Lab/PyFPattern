def split_host_pattern(pattern):
    "\n    Takes a string containing host patterns separated by commas (or a list\n    thereof) and returns a list of single patterns (which may not contain\n    commas). Whitespace is ignored.\n\n    Also accepts ':' as a separator for backwards compatibility, but it is\n    not recommended due to the conflict with IPv6 addresses and host ranges.\n\n    Example: 'a,b[1], c[2:3] , d' -> ['a', 'b[1]', 'c[2:3]', 'd']\n    "
    if isinstance(pattern, list):
        return list(itertools.chain(*map(split_host_pattern, pattern)))
    elif (not isinstance(pattern, string_types)):
        pattern = to_native(pattern)
    if (',' in pattern):
        patterns = pattern.split(',')
    else:
        try:
            (base, port) = parse_address(pattern, allow_ranges=True)
            patterns = [pattern]
        except:
            patterns = re.findall("(?:             # We want to match something comprising:\n                        [^\\s:\\[\\]]  # (anything other than whitespace or ':[]'\n                        |           # ...or...\n                        \\[[^\\]]*\\]  # a single complete bracketed expression)\n                    )+              # occurring once or more\n                ", pattern, re.X)
    return [p.strip() for p in patterns]