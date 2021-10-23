def add(self, lines, parents=None):
    ancestors = list()
    offset = 0
    obj = None
    if (not parents):
        for line in lines:
            item = ConfigLine(line)
            item.raw = line
            if (item not in self.items):
                self.items.append(item)
    else:
        for (index, p) in enumerate(parents):
            try:
                i = (index + 1)
                obj = self.get_section(parents[:i])[0]
                ancestors.append(obj)
            except ValueError:
                offset = (index * self._indent)
                obj = ConfigLine(p)
                obj.raw = p.rjust((len(p) + offset))
                if ancestors:
                    obj.parents = list(ancestors)
                    ancestors[(- 1)].children.append(obj)
                self.items.append(obj)
                ancestors.append(obj)
        for line in lines:
            for child in ancestors[(- 1)].children:
                if (child.text == line):
                    break
            else:
                offset = (len(parents) * self._indent)
                item = ConfigLine(line)
                item.raw = line.rjust((len(line) + offset))
                item._parents = ancestors
                ancestors[(- 1)].children.append(item)
                self.items.append(item)