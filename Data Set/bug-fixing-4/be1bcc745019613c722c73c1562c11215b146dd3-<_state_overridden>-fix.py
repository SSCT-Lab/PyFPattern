def _state_overridden(self, want, have):
    ' The command generator when state is overridden\n\n        :param want: the desired configuration as a dictionary\n        :param obj_in_have: the current configuration as a dictionary\n        :rtype: A list\n        :returns: the commands necessary to migrate the current configuration\n                  to the desired configuration\n        '
    commands = []
    for each in have:
        for interface in want:
            count = 0
            if (each['name'] == interface['name']):
                break
            elif (interface['name'] in each['name']):
                break
            count += 1
        else:
            interface = dict(name=each['name'])
            commands.extend(self._clear_config(interface, each))
            continue
        have_dict = filter_dict_having_none_value(interface, each)
        commands.extend(self._clear_config(dict(), have_dict))
        commands.extend(self._set_config(interface, each))
        del want[count]
    for each in want:
        commands.extend(self._set_config(each, dict()))
    commands = remove_duplicate_interface(commands)
    return commands