def import_module(self, name):
    try:
        modname = 'kivy.modules.{0}'.format(name)
        module = __import__(name=modname)
        module = sys.modules[modname]
    except ImportError:
        try:
            module = __import__(name=name)
            module = sys.modules[name]
        except ImportError:
            Logger.exception(('Modules: unable to import <%s>' % name))
            self.mods[name]['module'] = None
            return
    if (not hasattr(module, 'start')):
        Logger.warning(('Modules: Module <%s> missing start() function' % name))
        return
    if (not hasattr(module, 'stop')):
        err = ('Modules: Module <%s> missing stop() function' % name)
        Logger.warning(err)
        return
    self.mods[name]['module'] = module