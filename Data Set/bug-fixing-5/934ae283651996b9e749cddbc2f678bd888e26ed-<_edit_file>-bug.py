def _edit_file(self, filename, regexp, value):
    'Replace the first matched line with given `value`.\n\n        If `regexp` matched more than once, other than the first line will be deleted.\n\n        Args:\n            filename: The name of the file to edit.\n            regexp:   The regular expression to search with.\n            value:    The line which will be inserted.\n        '
    try:
        file = open(filename, 'r')
    except IOError:
        self.abort(('cannot read "%s"' % filename))
    else:
        lines = file.readlines()
        file.close()
    matched_indices = []
    for (i, line) in enumerate(lines):
        if regexp.search(line):
            matched_indices.append(i)
    if (len(matched_indices) > 0):
        insert_line = matched_indices[0]
    else:
        insert_line = 0
    for i in matched_indices[::(- 1)]:
        del lines[i]
    lines.insert(insert_line, value)
    try:
        file = open(filename, 'w')
    except IOError:
        self.abort(('cannot write to "%s"' % filename))
    else:
        file.writelines(lines)
        file.close()
    self.msg.append(('Added 1 line and deleted %s line(s) on %s' % (len(matched_indices), filename)))