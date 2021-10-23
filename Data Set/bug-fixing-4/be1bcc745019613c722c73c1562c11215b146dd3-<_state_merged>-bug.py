def _state_merged(self, want, have):
    ' The command generator when state is merged\n\n        :param want: the additive configuration as a dictionary\n        :param obj_in_have: the current configuration as a dictionary\n        :rtype: A list\n        :returns: the commands necessary to merge the provided into\n                  the current configuration\n        '
    commands = []
    for interface in want:
        for each in have:
            if (each['name'] == interface['name']):
                break
        else:
            continue
        commands.extend(self._set_config(interface, each))
    return commands