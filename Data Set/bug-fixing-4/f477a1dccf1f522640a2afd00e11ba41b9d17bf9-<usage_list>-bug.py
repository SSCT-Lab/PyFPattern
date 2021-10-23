def usage_list(self):
    print()
    print('Available modules')
    print('=================')
    for module in self.list():
        if ('module' not in self.mods[module]):
            self.import_module(module)
        text = self.mods[module]['module'].__doc__.strip('\n ')
        print(('%-12s: %s' % (module, text)))
    print()