

def _post_validate_environment(self, attr, value, templar):
    "\n        Override post validation of vars on the play, as we don't want to\n        template these too early.\n        "
    if (value is None):
        return dict()
    elif isinstance(value, list):
        if (len(value) == 1):
            return templar.template(value[0], convert_bare=True)
        else:
            env = []
            for env_item in value:
                if (isinstance(env_item, (string_types, AnsibleUnicode)) and (env_item in templar._available_variables.keys())):
                    env[env_item] = templar.template(env_item, convert_bare=True)
    elif isinstance(value, dict):
        env = dict()
        for env_item in value:
            if (isinstance(env_item, (string_types, AnsibleUnicode)) and (env_item in templar._available_variables.keys())):
                env[env_item] = templar.template(value[env_item], convert_bare=True)
    return templar.template(value, convert_bare=True)
