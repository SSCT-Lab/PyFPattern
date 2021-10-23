def __init__(self, min_pandevice_version, min_panos_version, panorama_error, firewall_error):
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
    self.min_pandevice_version = min_pandevice_version
    self.min_panos_version = min_panos_version
    self.panorama_error = panorama_error
    self.firewall_error = firewall_error
    self.device = None