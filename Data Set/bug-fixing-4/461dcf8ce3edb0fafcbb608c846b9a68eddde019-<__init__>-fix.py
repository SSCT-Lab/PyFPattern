def __init__(self, argument_spec, bypass_checks=False, no_log=False, check_invalid_arguments=True, mutually_exclusive=None, required_together=None, required_one_of=None, add_file_common_args=False, supports_check_mode=False, required_if=None):
    '\n        common code for quickly building an ansible module in Python\n        (although you can write modules in anything that can return JSON)\n        see library/* for examples\n        '
    self._name = os.path.basename(__file__)
    self.argument_spec = argument_spec
    self.supports_check_mode = supports_check_mode
    self.check_mode = False
    self.no_log = no_log
    self.cleanup_files = []
    self._debug = False
    self._diff = False
    self._verbosity = 0
    self.run_command_environ_update = {
        
    }
    self.aliases = {
        
    }
    self._legal_inputs = ['_ansible_check_mode', '_ansible_no_log', '_ansible_debug', '_ansible_diff', '_ansible_verbosity', '_ansible_selinux_special_fs', '_ansible_module_name', '_ansible_version', '_ansible_syslog_facility']
    if add_file_common_args:
        for (k, v) in FILE_COMMON_ARGUMENTS.items():
            if (k not in self.argument_spec):
                self.argument_spec[k] = v
    self._load_params()
    self._set_fallbacks()
    try:
        self.aliases = self._handle_aliases()
    except Exception:
        e = get_exception()
        print(('\n{"failed": true, "msg": "Module alias error: %s"}' % str(e)))
        sys.exit(1)
    self.no_log_values = set()
    for (arg_name, arg_opts) in self.argument_spec.items():
        if arg_opts.get('no_log', False):
            no_log_object = self.params.get(arg_name, None)
            if no_log_object:
                self.no_log_values.update(return_values(no_log_object))
    self._check_locale()
    self._check_arguments(check_invalid_arguments)
    if (not bypass_checks):
        self._check_mutually_exclusive(mutually_exclusive)
    self._set_defaults(pre=True)
    self._CHECK_ARGUMENT_TYPES_DISPATCHER = {
        'str': self._check_type_str,
        'list': self._check_type_list,
        'dict': self._check_type_dict,
        'bool': self._check_type_bool,
        'int': self._check_type_int,
        'float': self._check_type_float,
        'path': self._check_type_path,
        'raw': self._check_type_raw,
        'jsonarg': self._check_type_jsonarg,
        'json': self._check_type_jsonarg,
        'bytes': self._check_type_bytes,
        'bits': self._check_type_bits,
    }
    if (not bypass_checks):
        self._check_required_arguments()
        self._check_argument_types()
        self._check_argument_values()
        self._check_required_together(required_together)
        self._check_required_one_of(required_one_of)
        self._check_required_if(required_if)
    self._set_defaults(pre=False)
    if (not self.no_log):
        self._log_invocation()
    self._set_cwd()