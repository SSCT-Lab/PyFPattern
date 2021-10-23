

def filter_targets(targets, patterns, include=True, directories=True, errors=True):
    '\n    :type targets: collections.Iterable[CompletionTarget]\n    :type patterns: list[str]\n    :type include: bool\n    :type directories: bool\n    :type errors: bool\n    :rtype: collections.Iterable[CompletionTarget]\n    '
    unmatched = set((patterns or ()))
    compiled_patterns = (dict(((p, re.compile(('^%s$' % p))) for p in patterns)) if patterns else None)
    for target in targets:
        matched_directories = set()
        match = False
        if patterns:
            for alias in target.aliases:
                for pattern in patterns:
                    if compiled_patterns[pattern].match(alias):
                        match = True
                        try:
                            unmatched.remove(pattern)
                        except KeyError:
                            pass
                        if alias.endswith('/'):
                            if (target.base_path and (len(target.base_path) > len(alias))):
                                matched_directories.add(target.base_path)
                            else:
                                matched_directories.add(alias)
        elif include:
            match = True
            if (not target.base_path):
                matched_directories.add('.')
            for alias in target.aliases:
                if alias.endswith('/'):
                    if (target.base_path and (len(target.base_path) > len(alias))):
                        matched_directories.add(target.base_path)
                    else:
                        matched_directories.add(alias)
        if (match != include):
            continue
        if (directories and matched_directories):
            (yield DirectoryTarget(sorted(matched_directories, key=len)[0], target.modules))
        else:
            (yield target)
    if errors:
        if unmatched:
            raise TargetPatternsNotMatched(unmatched)
