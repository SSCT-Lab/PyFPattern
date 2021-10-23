def exec_module(self, **kwargs):
    for key in list(self.module_arg_spec):
        setattr(self, key, kwargs[key])
    if (self.resource_group and self.name):
        self.results['autoscales'] = self.get()
    elif self.resource_group:
        self.results['autoscales'] = self.list_by_resource_group()
    return self.results