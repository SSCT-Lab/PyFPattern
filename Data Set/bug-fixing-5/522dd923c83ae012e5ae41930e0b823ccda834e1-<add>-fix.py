def add(self, lines, parents=None):
    ancestors = list()
    offset = 0
    obj = None
    if (not parents):
        for line in lines:
            if ignore_line(line):
                continue
            item = ConfigLine(line)
            item.raw = line
            if (item not in self.items):
                self.items.append(item)
    else:
        for (index, p) in enumerate(parents):
            try:
                i = (index + 1)
                obj = self.get_block(parents[:i])[0]
                ancestors.append(obj)
            except ValueError:
                offset = (index * self._indent)
                obj = ConfigLine(p)
                obj.raw = p.rjust((len(p) + offset))
                if ancestors:
                    obj._parents = list(ancestors)
                    ancestors[(- 1)]._children.append(obj)
                self.items.append(obj)
                ancestors.append(obj)
        for line in lines:
            if ignore_line(line):
                continue
            for child in ancestors[(- 1)]._children:
                if (child.text == line):
                    break
            else:
                offset = (len(parents) * self._indent)
                item = ConfigLine(line)
                item.raw = line.rjust((len(line) + offset))
                item._parents = ancestors
                ancestors[(- 1)]._children.append(item)
                self.items.append(item)