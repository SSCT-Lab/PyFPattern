

def __init__(self, module):
    '\n        Constructor\n        '
    if (not HAS_REQUESTS):
        self.module.fail_json(msg="Unable to find 'requests' Python library which is required. Please install using 'pip install requests'")
    if (not HAS_PYVMOMI):
        module.fail_json(msg='PyVmomi Python module required. Install using "pip install PyVmomi"')
    self.module = module
    self.params = module.params
    self.si = None
    self.current_vm_obj = None
    self.content = connect_to_api(self.module)
