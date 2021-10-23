def sudorule_add_allow_command(self, name, item):
    return self._post_json(method='sudorule_add_allow_command', name=name, item={
        'sudocmd': item,
    })