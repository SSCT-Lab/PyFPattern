

def __init__(self, loader, shared_loader_obj=None, variables=dict()):
    self._loader = loader
    self._filters = None
    self._tests = None
    self._available_variables = variables
    self._cached_result = {
        
    }
    if loader:
        self._basedir = loader.get_basedir()
    else:
        self._basedir = './'
    if shared_loader_obj:
        self._filter_loader = getattr(shared_loader_obj, 'filter_loader')
        self._test_loader = getattr(shared_loader_obj, 'test_loader')
        self._lookup_loader = getattr(shared_loader_obj, 'lookup_loader')
    else:
        self._filter_loader = filter_loader
        self._test_loader = test_loader
        self._lookup_loader = lookup_loader
    self._fail_on_lookup_errors = True
    self._fail_on_filter_errors = True
    self._fail_on_undefined_errors = C.DEFAULT_UNDEFINED_VAR_BEHAVIOR
    self.environment = Environment(trim_blocks=True, undefined=StrictUndefined, extensions=self._get_extensions(), finalize=self._finalize, loader=FileSystemLoader(self._basedir))
    self.environment.template_class = AnsibleJ2Template
    self.SINGLE_VAR = re.compile(('^%s\\s*(\\w*)\\s*%s$' % (self.environment.variable_start_string, self.environment.variable_end_string)))
    self.block_start = self.environment.block_start_string
    self.block_end = self.environment.block_end_string
    self.variable_start = self.environment.variable_start_string
    self.variable_end = self.environment.variable_end_string
    self._clean_regex = re.compile(('(?:%s|%s|%s|%s)' % (self.variable_start, self.block_start, self.block_end, self.variable_end)))
    self._no_type_regex = re.compile(('.*\\|\\s*(?:%s)\\s*(?:%s)?$' % ('|'.join(C.STRING_TYPE_FILTERS), self.variable_end)))
