def my_represent_scalar(self, tag, value, style=None):
    'Uses block style for multi-line strings'
    if (style is None):
        if should_use_block(value):
            style = '|'
            value = value.rstrip()
            value = ''.join((x for x in value if (x in string.printable)))
            value = value.expandtabs()
            value = re.sub('[\\x0b\\x0c\\r]', '', value)
            value = re.sub(' +\\n', '\n', value)
        else:
            style = self.default_style
    node = yaml.representer.ScalarNode(tag, value, style=style)
    if (self.alias_key is not None):
        self.represented_objects[self.alias_key] = node
    return node