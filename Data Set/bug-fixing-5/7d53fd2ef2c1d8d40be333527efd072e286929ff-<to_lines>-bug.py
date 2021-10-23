def to_lines(self, section):
    lines = list()
    for entry in section[1:]:
        line = ['set']
        line.extend([p.text for p in entry.parents])
        line.append(entry.text)
        lines.append(' '.join(line))
    return lines