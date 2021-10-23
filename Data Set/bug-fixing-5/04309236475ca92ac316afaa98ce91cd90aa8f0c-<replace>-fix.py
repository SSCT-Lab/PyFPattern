def replace(self, patterns, repl, parents=None, add_if_missing=False, ignore_whitespace=True):
    match = None
    parents = (to_list(parents) or list())
    patterns = [re.compile(r, re.I) for r in to_list(patterns)]
    for item in self.items:
        for regexp in patterns:
            text = item.text
            if (not ignore_whitespace):
                text = item.raw
            if regexp.search(text):
                if (item.text != repl):
                    if (parents == [p.text for p in item.parents]):
                        match = item
                        break
    if match:
        match.text = repl
        indent = (len(match.raw) - len(match.raw.lstrip()))
        match.raw = repl.rjust((len(repl) + indent))
    elif add_if_missing:
        self.add(repl, parents=parents)