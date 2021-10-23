def __init__(self):
    self.module_arg_spec = dict(resource_group_name=dict(type='str', required=True, aliases=['resource_group']), state=dict(type='str', default='present', choices=['present', 'absent']), template=dict(type='dict', default=None), parameters=dict(type='dict', default=None), template_link=dict(type='str', default=None), parameters_link=dict(type='str', default=None), location=dict(type='str', default='westus'), deployment_mode=dict(type='str', default='incremental', choices=['complete', 'incremental']), deployment_name=dict(type='str', default='ansible-arm'), wait_for_deployment_completion=dict(type='bool', default=True), wait_for_deployment_polling_period=dict(type='int', default=10))
    mutually_exclusive = [('template', 'template_link'), ('parameters', 'parameters_link')]
    self.resource_group_name = None
    self.state = None
    self.template = None
    self.parameters = None
    self.template_link = None
    self.parameters_link = None
    self.location = None
    self.deployment_mode = None
    self.deployment_name = None
    self.wait_for_deployment_completion = None
    self.wait_for_deployment_polling_period = None
    self.tags = None
    self.append_tags = None
    self.results = dict(deployment=dict(), changed=False, msg='')
    super(AzureRMDeploymentManager, self).__init__(derived_arg_spec=self.module_arg_spec, mutually_exclusive=mutually_exclusive, supports_check_mode=False)