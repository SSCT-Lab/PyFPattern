@staticmethod
def _get_value(param_name, param_value, env_variable, default_value):
    if (param_value is not None):
        if (param_value in BOOLEANS_TRUE):
            return True
        if (param_value in BOOLEANS_FALSE):
            return False
        return param_value
    if (env_variable is not None):
        env_value = os.environ.get(env_variable)
        if (env_value is not None):
            if (param_name == 'cert_path'):
                return os.path.join(env_value, 'cert.pem')
            if (param_name == 'cacert_path'):
                return os.path.join(env_value, 'ca.pem')
            if (param_name == 'key_path'):
                return os.path.join(env_value, 'key.pem')
            if (env_value in BOOLEANS_TRUE):
                return True
            if (env_value in BOOLEANS_FALSE):
                return False
            return env_value
    return default_value