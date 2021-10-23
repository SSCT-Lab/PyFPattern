def usage_list(self):
    print('Available modules')
    print('=================')
    for module in sorted(self.list()):
        if ('module' not in self.mods[module]):
            self.import_module(module)
        if (not self.mods[module]['module'].__doc__):
            continue
        text = self.mods[module]['module'].__doc__.strip('\n ')
        text = text.split('\n')
        if (len(text) > 2):
            if text[1].startswith('='):
                text[1] = ('=' * (14 + len(text[1])))
        text = '\n'.join(text)
        print(('\n%-12s: %s' % (module, text)))