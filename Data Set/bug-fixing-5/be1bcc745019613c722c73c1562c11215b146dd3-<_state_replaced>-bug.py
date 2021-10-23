def _state_replaced(self, want, have):
    ' The command generator when state is replaced\n\n        :param want: the desired configuration as a dictionary\n        :param have: the current configuration as a dictionary\n        :param interface_type: interface type\n        :rtype: A list\n        :returns: the commands necessary to migrate the current configuration\n                  to the deisred configuration\n        '
    commands = []
    for interface in want:
        for each in have:
            if (each['name'] == interface['name']):
                break
            elif (interface['name'] in each['name']):
                break
        else:
            continue
        have_dict = filter_dict_having_none_value(interface, each)
        want = dict()
        commands.extend(self._clear_config(want, have_dict))
        commands.extend(self._set_config(interface, each))
    commands = remove_duplicate_interface(commands)
    return commands