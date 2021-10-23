def _load_from_state_dict(self, state_dict, prefix, strict, missing_keys, unexpected_keys, error_msgs):
    'Copies parameters and buffers from :attr:`state_dict` into only\n        this module, but not its descendants. This is called on every submodule\n        in :meth:`~torch.nn.Module.load_state_dict`. Metadata saved for this\n        module in input :attr:`state_dict` is at ``state_dict._metadata[prefix]``.\n        Subclasses can achieve class-specific backward compatible loading using\n        the version number at ``state_dict._metadata[prefix]["version"]``.\n\n        .. note::\n            :attr:`state_dict` is not the same object as the input\n            :attr:`state_dict` to :meth:`~torch.nn.Module.load_state_dict`. So\n            it can be modified.\n\n        Arguments:\n            state_dict (dict): a dict containing parameters and\n                persistent buffers.\n            prefix (str): the prefix for parameters and buffers used in this\n                module\n            strict (bool): whether to strictly enforce that the keys in\n                :attr:`state_dict` with :attr:`prefix` match the names of\n                parameters and buffers in this module\n            missing_keys (list of str): if ``strict=False``, add missing keys to\n                this list\n            unexpected_keys (list of str): if ``strict=False``, add unexpected\n                keys to this list\n            error_msgs (list of str): error messages should be added to this\n                list, and will be reported together in\n                :meth:`~torch.nn.Module.load_state_dict`\n        '
    local_name_params = itertools.chain(self._parameters.items(), self._buffers.items())
    local_state = {k: v.data for (k, v) in local_name_params if (v is not None)}
    for (name, param) in local_state.items():
        key = (prefix + name)
        if (key in state_dict):
            input_param = state_dict[key]
            if (input_param.shape != param.shape):
                error_msgs.append('Size mismatch: copying a param of {} from checkpoint, where the shape is {} in current model.'.format(param.shape, input_param.shape))
            if isinstance(input_param, Parameter):
                input_param = input_param.data
            try:
                param.copy_(input_param)
            except Exception:
                error_msgs.append('While copying the parameter named "{}", whose dimensions in the model are {} and whose dimensions in the checkpoint are {}.'.format(key, param.size(), input_param.size()))
        elif strict:
            missing_keys.append(key)
    if strict:
        for (key, input_param) in state_dict.items():
            if key.startswith(prefix):
                input_name = key[len(prefix):]
                input_name = input_name.split('.', 1)[0]
                if ((input_name not in self._modules) and (input_name not in local_state)):
                    unexpected_keys.append(key)