def replace(self, replace, text=None, regex=None, parents=None, add_if_missing=False, ignore_whitespace=False):
    match = None
    parents = (parents or list())
    if ((text is None) and (regex is None)):
        raise ValueError('missing required arguments')
    if (not regex):
        regex = [('^%s$' % text)]
    patterns = [re.compile(r, re.I) for r in to_list(regex)]
    for item in self.items:
        for regexp in patterns:
            string = (((ignore_whitespace is True) and item.text) or item.raw)
            if regexp.search(item.text):
                if (item.text != replace):
                    if (parents == [p.text for p in item.parents]):
                        match = item
                        break
    if match:
        match.text = replace
        indent = (len(match.raw) - len(match.raw.lstrip()))
        match.raw = replace.rjust((len(replace) + indent))
    elif add_if_missing:
        self.add(replace, parents=parents)