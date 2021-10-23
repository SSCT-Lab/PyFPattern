def common_environment():
    'Common environment used for executing all programs.'
    env = dict(LC_ALL='en_US.UTF-8', PATH=os.environ.get('PATH', os.defpath))
    required = ('HOME',)
    optional = ('HTTPTESTER', 'SSH_AUTH_SOCK')
    env.update(pass_vars(required=required, optional=optional))
    return env