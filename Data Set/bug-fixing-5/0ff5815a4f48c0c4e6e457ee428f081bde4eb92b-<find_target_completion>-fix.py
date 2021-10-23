def find_target_completion(target_func, prefix):
    '\n    :type target_func: () -> collections.Iterable[CompletionTarget]\n    :type prefix: unicode\n    :rtype: list[str]\n    '
    try:
        targets = target_func()
        if (sys.version_info[0] == 2):
            prefix = prefix.encode()
        short = (os.environ.get('COMP_TYPE') == '63')
        matches = walk_completion_targets(targets, prefix, short)
        return matches
    except Exception as ex:
        return [str(ex)]