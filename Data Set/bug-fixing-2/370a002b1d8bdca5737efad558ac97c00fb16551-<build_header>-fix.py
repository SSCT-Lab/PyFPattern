

def build_header(self, plugin, attribute, stat):
    'Build and return the header line'
    line = ''
    if (attribute is not None):
        line += '{}.{}{}'.format(plugin, attribute, self.separator)
    elif isinstance(stat, dict):
        for k in stat.keys():
            line += '{}.{}{}'.format(plugin, str(k), self.separator)
    elif isinstance(stat, list):
        for i in stat:
            if (isinstance(i, dict) and ('key' in i)):
                for k in i.keys():
                    line += '{}.{}.{}{}'.format(plugin, str(i['key']), str(k), self.separator)
    else:
        line += '{}{}'.format(plugin, self.separator)
    return line
