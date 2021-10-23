def __init__(self, loader, variable_manager, host_list=C.DEFAULT_HOST_LIST):
    self.host_list = host_list
    self._loader = loader
    self._variable_manager = variable_manager
    self._vars_per_host = {
        
    }
    self._vars_per_group = {
        
    }
    self._hosts_cache = {
        
    }
    self._pattern_cache = {
        
    }
    self._vars_plugins = []
    self._playbook_basedir = None
    self.groups = {
        
    }
    self._restriction = None
    self._subset = None
    self.clear_pattern_cache()
    self.parse_inventory(host_list)