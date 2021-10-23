def parse(self, lines, comment_tokens=None):
    toplevel = re.compile('\\S')
    childline = re.compile('^\\s*(.+)$')
    entry_reg = re.compile('([{};])')
    ancestors = list()
    config = list()
    curlevel = 0
    prevlevel = 0
    for (linenum, line) in enumerate(to_native(lines, errors='surrogate_or_strict').split('\n')):
        text = entry_reg.sub('', line).strip()
        cfg = ConfigLine(line)
        if ((not text) or ignore_line(text, comment_tokens)):
            continue
        if toplevel.match(line):
            ancestors = [cfg]
            prevlevel = curlevel
            curlevel = 0
        else:
            match = childline.match(line)
            line_indent = match.start(1)
            prevlevel = curlevel
            curlevel = int((line_indent / self._indent))
            if ((curlevel - 1) > prevlevel):
                curlevel = (prevlevel + 1)
            parent_level = (curlevel - 1)
            cfg._parents = ancestors[:curlevel]
            if (curlevel > len(ancestors)):
                config.append(cfg)
                continue
            for i in range(curlevel, len(ancestors)):
                ancestors.pop()
            ancestors.append(cfg)
            ancestors[parent_level].add_child(cfg)
        config.append(cfg)
    return config