def _compare_condition(self, current_conditions, condition):
    '\n\n        :param current_conditions:\n        :param condition:\n        :return:\n        '
    condition_found = False
    for current_condition in current_conditions:
        if current_condition.get('SourceIpConfig'):
            if ((current_condition['Field'] == condition['Field']) and (current_condition['SourceIpConfig']['Values'][0] == condition['SourceIpConfig']['Values'][0])):
                condition_found = True
                break
        elif ((current_condition['Field'] == condition['Field']) and (sorted(current_condition['Values']) == sorted(condition['Values']))):
            condition_found = True
            break
    return condition_found