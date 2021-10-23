def _vector_str(self, indent, fmt, scale, sz, summarize):
    element_length = (sz + 3)
    elements_per_line = int(math.floor(((PRINT_OPTS.linewidth - indent) / element_length)))
    char_per_line = (element_length * elements_per_line)
    if (summarize and (self.size(0) > (2 * PRINT_OPTS.edgeitems))):
        data = (([fmt((val / scale)) for val in self[:PRINT_OPTS.edgeitems].tolist()] + [' ...']) + [fmt((val / scale)) for val in self[(- PRINT_OPTS.edgeitems):].tolist()])
    else:
        data = [fmt((val / scale)) for val in self.tolist()]
    data_lines = [data[i:(i + elements_per_line)] for i in range(0, len(data), elements_per_line)]
    lines = [', '.join(line) for line in data_lines]
    return (('[' + ((',' + '\n') + (' ' * (indent + 1))).join(lines)) + ']')