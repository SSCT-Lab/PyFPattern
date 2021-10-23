def select_resource_pool(self, host):
    resource_pools = get_all_objs(self.content, [vim.ResourcePool])
    for rp in resource_pools.items():
        if (not rp[0]):
            continue
        if (not hasattr(rp[0], 'parent')):
            continue
        if self.obj_has_parent(rp[0].parent, host.parent):
            if ((self.module.params['resource_pool'] is None) or (rp[0].name == self.module.params['resource_pool'])):
                return rp[0]
    if (self.module.params['resource_pool'] is not None):
        self.module.fail_json(msg=('Could not find resource_pool %s for selected host %s' % (self.module.params['resource_pool'], host.name)))
    else:
        self.module.fail_json(msg=('Failed to find a resource group for %s' % host.name))