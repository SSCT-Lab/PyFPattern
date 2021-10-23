def populate(self, installed_apps=None):
    '\n        Loads application configurations and models.\n\n        This method imports each application module and then each model module.\n\n        It is thread safe and idempotent, but not reentrant.\n        '
    if self.ready:
        return
    with self._lock:
        if self.ready:
            return
        if self.app_configs:
            raise RuntimeError("populate() isn't reentrant")
        for entry in installed_apps:
            if isinstance(entry, AppConfig):
                app_config = entry
            else:
                app_config = AppConfig.create(entry)
            if (app_config.label in self.app_configs):
                raise ImproperlyConfigured(("Application labels aren't unique, duplicates: %s" % app_config.label))
            self.app_configs[app_config.label] = app_config
            app_config.apps = self
        counts = Counter((app_config.name for app_config in self.app_configs.values()))
        duplicates = [name for (name, count) in counts.most_common() if (count > 1)]
        if duplicates:
            raise ImproperlyConfigured(("Application names aren't unique, duplicates: %s" % ', '.join(duplicates)))
        self.apps_ready = True
        for app_config in self.app_configs.values():
            app_config.import_models()
        self.clear_cache()
        self.models_ready = True
        for app_config in self.get_app_configs():
            app_config.ready()
        self.ready = True