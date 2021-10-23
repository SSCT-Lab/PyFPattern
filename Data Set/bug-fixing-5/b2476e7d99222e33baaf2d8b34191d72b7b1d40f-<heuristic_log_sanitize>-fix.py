def heuristic_log_sanitize(data, no_log_values=None):
    ' Remove strings that look like passwords from log messages '
    data = to_native(data)
    output = []
    begin = len(data)
    prev_begin = begin
    sep = 1
    while sep:
        try:
            end = data.rindex('@', 0, begin)
        except ValueError:
            output.insert(0, data[0:begin])
            break
        sep = None
        sep_search_end = end
        while (not sep):
            try:
                begin = data.rindex('://', 0, sep_search_end)
            except ValueError:
                begin = 0
            try:
                sep = data.index(':', (begin + 3), end)
            except ValueError:
                if (begin == 0):
                    output.insert(0, data[0:begin])
                    break
                sep_search_end = begin
                continue
        if sep:
            output.insert(0, data[end:prev_begin])
            output.insert(0, '********')
            output.insert(0, data[begin:(sep + 1)])
            prev_begin = begin
    output = ''.join(output)
    if no_log_values:
        output = remove_values(output, no_log_values)
    return output