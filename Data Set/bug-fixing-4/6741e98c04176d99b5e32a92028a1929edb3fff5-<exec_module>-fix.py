def exec_module(self, **kwargs):
    for key in (list(self.module_arg_spec.keys()) + ['append_tags', 'tags']):
        setattr(self, key, kwargs[key])
    if (self.state == 'present'):
        deployment = self.deploy_template()
        if (deployment is None):
            self.results['deployment'] = dict(name=self.deployment_name, group_name=self.resource_group_name, id=None, outputs=None, instances=None)
        else:
            self.results['deployment'] = dict(name=deployment.name, group_name=self.resource_group_name, id=deployment.id, outputs=deployment.properties.outputs, instances=self._get_instances(deployment))
        self.results['changed'] = True
        self.results['msg'] = 'deployment succeeded'
    else:
        try:
            if self.get_resource_group(self.resource_group_name):
                self.destroy_resource_group()
                self.results['changed'] = True
                self.results['msg'] = 'deployment deleted'
        except CloudError:
            pass
    return self.results