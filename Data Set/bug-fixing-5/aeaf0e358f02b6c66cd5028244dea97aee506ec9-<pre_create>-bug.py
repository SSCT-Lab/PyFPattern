def pre_create(self, entity):
    if (entity is None):
        if (self.param('template') is None):
            self._module.params['template'] = 'Blank'