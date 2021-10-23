def __init__(self, installed_apps=()):
    if ((installed_apps is None) and hasattr(sys.modules[__name__], 'apps')):
        raise RuntimeError('You must supply an installed_apps argument.')
    self.all_models = defaultdict(OrderedDict)
    self.app_configs = OrderedDict()
    self.stored_app_configs = []
    self.apps_ready = self.models_ready = self.ready = False
    self._lock = threading.RLock()
    self.loading = False
    self._pending_operations = defaultdict(list)
    if (installed_apps is not None):
        self.populate(installed_apps)