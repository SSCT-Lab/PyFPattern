def __init__(self, panorama_error, firewall_error):
    'Performs connection initialization and determines params.'
    self.argument_spec = {
        
    }
    self.required_one_of = []
    self.vsys = None
    self.device_group = None
    self.vsys_dg = None
    self.rulebase = None
    self.template = None
    self.template_stack = None
    self.vsys_importable = None
    self.panorama_error = panorama_error
    self.firewall_error = firewall_error
    self.device = None