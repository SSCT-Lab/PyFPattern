def to_lines(self, objects):
    lines = list()
    for obj in objects:
        line = list()
        line.extend([p.text for p in obj.parents])
        line.append(obj.text)
        lines.append(' '.join(line))
    return lines