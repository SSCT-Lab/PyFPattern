def load_state_dict(self, state_dict):
    'Loads the optimizer state.\n\n        Arguments:\n            state_dict (dict): optimizer state. Should be an object returned\n                from a call to :meth:`state_dict`.\n        '
    state_dict = deepcopy(state_dict)
    groups = self.param_groups
    saved_groups = state_dict['param_groups']
    if (len(groups) != len(saved_groups)):
        raise ValueError('loaded state dict has a different number of parameter groups')
    param_lens = (len(g['params']) for g in groups)
    saved_lens = (len(g['params']) for g in saved_groups)
    if any(((p_len != s_len) for (p_len, s_len) in zip(param_lens, saved_lens))):
        raise ValueError("loaded state dict contains a parameter group that doesn't match the size of optimizer's group")
    id_map = {old_id: p for (old_id, p) in zip(chain(*(g['params'] for g in saved_groups)), chain(*(g['params'] for g in groups)))}
    state = {id_map.get(k, k): v for (k, v) in state_dict['state'].items()}

    def update_group(group, new_group):
        new_group['params'] = group['params']
        return new_group
    param_groups = [update_group(g, ng) for (g, ng) in zip(groups, saved_groups)]
    self.__setstate__({
        'state': state,
        'param_groups': param_groups,
    })