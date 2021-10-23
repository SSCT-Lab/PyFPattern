def build_table(events, sort_by=None, header=None):
    'Prints a summary of events (which can be a list of FunctionEvent or FunctionEventAvg).'
    if (sort_by is not None):
        events = sorted(events, key=(lambda evt: getattr(evt, sort_by)))
    max_name_length = max((len(evt.key) for evt in events))
    max_name_length += 4
    col_width = 15
    col_format = (('  {: >' + str(col_width)) + '}')
    row_format = ((('{: <' + str(max_name_length)) + '}') + (col_format * 5))
    header_sep = (('-' * max_name_length) + (('  ' + ('-' * col_width)) * 5))
    result = ['']

    def append(s):
        result[0] += s
        result[0] += '\n'
    if (header is not None):
        line_length = (max_name_length + ((col_width + 2) * 5))
        append(('=' * line_length))
        append(header)
    append(header_sep)
    append(row_format.format('Name', 'CPU time', 'CUDA time', 'Calls', 'CPU total', 'CUDA total'))
    append(header_sep)
    for evt in events:
        append(row_format.format(evt.key, evt.cpu_time_str, evt.cuda_time_str, evt.count, evt.cpu_time_total_str, evt.cuda_time_total_str))
    return result[0]