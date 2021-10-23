def set_installed_apps(self, installed):
    "\n        Enables a different set of installed apps for get_app_config[s].\n\n        installed must be an iterable in the same format as INSTALLED_APPS.\n\n        set_installed_apps() must be balanced with unset_installed_apps(),\n        even if it exits with an exception.\n\n        Primarily used as a receiver of the setting_changed signal in tests.\n\n        This method may trigger new imports, which may add new models to the\n        registry of all imported models. They will stay in the registry even\n        after unset_installed_apps(). Since it isn't possible to replay\n        imports safely (eg. that could lead to registering listeners twice),\n        models are registered when they're imported and never removed.\n        "
    if (not self.ready):
        raise AppRegistryNotReady("App registry isn't ready yet.")
    self.stored_app_configs.append(self.app_configs)
    self.app_configs = OrderedDict()
    self.apps_ready = self.models_ready = self.ready = False
    self.clear_cache()
    self.populate(installed)