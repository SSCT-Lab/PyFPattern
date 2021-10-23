

@contextmanager
def setup_env(filename):
    pre_sys_modules = list(sys.modules.keys())
    fake = _FakeAnsibleModuleInit()
    module = __import__('ansible.module_utils.basic').module_utils.basic
    _original_init = module.AnsibleModule.__init__
    _original_load_params = module._load_params
    setattr(module.AnsibleModule, '__init__', fake)
    setattr(module, '_load_params', _fake_load_params)
    try:
        (yield fake)
    finally:
        setattr(module.AnsibleModule, '__init__', _original_init)
        setattr(module, '_load_params', _original_load_params)
        for k in list(sys.modules.keys()):
            if ((k not in pre_sys_modules) and k.startswith('ansible.module_utils.')):
                del sys.modules[k]
