def _compare_rule(self, current_rule, new_rule):
    '\n\n        :return:\n        '
    modified_rule = {
        
    }
    if (int(current_rule['Priority']) != int(new_rule['Priority'])):
        modified_rule['Priority'] = new_rule['Priority']
    if (len(current_rule['Actions']) > 1):
        for action in current_rule['Actions']:
            if ('Order' not in action):
                self.module.fail_json(msg="'Order' key not found in actions. installed version of botocore does not support multiple actions, please upgrade botocore to version 1.10.30 or higher")
    if (len(current_rule['Actions']) == len(new_rule['Actions'])):
        if ((len(current_rule['Actions']) == 1) and (len(new_rule['Actions']) == 1)):
            if (current_rule['Actions'] != new_rule['Actions']):
                modified_rule['Actions'] = new_rule['Actions']
        else:
            current_actions_sorted = sorted(current_rule['Actions'], key=(lambda x: x['Order']))
            new_actions_sorted = sorted(new_rule['Actions'], key=(lambda x: x['Order']))
            new_actions_sorted_no_secret = []
            for action in new_actions_sorted:
                if (action['Type'] == 'authenticate-oidc'):
                    action['AuthenticateOidcConfig'].pop('ClientSecret')
                    new_actions_sorted_no_secret.append(action)
                else:
                    new_actions_sorted_no_secret.append(action)
            if (current_actions_sorted != new_actions_sorted_no_secret):
                modified_rule['Actions'] = new_rule['Actions']
    else:
        modified_rule['Actions'] = new_rule['Actions']
    modified_conditions = []
    for condition in new_rule['Conditions']:
        if (not self._compare_condition(current_rule['Conditions'], condition)):
            modified_conditions.append(condition)
    if modified_conditions:
        modified_rule['Conditions'] = modified_conditions
    return modified_rule