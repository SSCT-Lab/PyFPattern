

def update_vars(self, variables):
    "\n        Adds 'magic' variables relating to connections to the variable dictionary provided.\n        In case users need to access from the play, this is a legacy from runner.\n        "
    for (prop, var_list) in MAGIC_VARIABLE_MAPPING.items():
        try:
            if ('become' in prop):
                continue
            var_val = getattr(self, prop)
            for var_opt in var_list:
                if ((var_opt not in variables) and (var_val is not None)):
                    variables[var_opt] = var_val
        except AttributeError:
            continue
