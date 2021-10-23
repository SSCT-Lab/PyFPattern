def add(self, lines, parents=None):
    offset = 0
    config = list()
    parent = None
    parents = (parents or list())
    for item in parents:
        line = ConfigLine(item)
        line.raw = item.rjust((len(item) + offset))
        config.append(line)
        if parent:
            parent.children.append(line)
            line.parents.append(parent)
        parent = line
        offset += self.indent
    self._config.extend(config)
    self._config.extend(list(self._build_children(lines, config, offset)))