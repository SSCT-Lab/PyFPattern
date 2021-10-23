

def node_update(self):
    if (not self.client.check_if_swarm_node(node_id=self.parameters.hostname)):
        self.client.fail('This node is not part of a swarm.')
        return
    if self.client.check_if_swarm_node_is_down():
        self.client.fail('Can not update the node. The node is down.')
    try:
        node_info = self.client.inspect_node(node_id=self.parameters.hostname)
    except APIError as exc:
        self.client.fail(('Failed to get node information for %s' % to_native(exc)))
    changed = False
    node_spec = dict(Availability=self.parameters.availability, Role=self.parameters.role, Labels=self.parameters.labels)
    if (self.parameters.role is None):
        node_spec['Role'] = node_info['Spec']['Role']
    elif (not (node_info['Spec']['Role'] == self.parameters.role)):
        node_spec['Role'] = self.parameters.role
        changed = True
    if (self.parameters.availability is None):
        node_spec['Availability'] = node_info['Spec']['Availability']
    elif (not (node_info['Spec']['Availability'] == self.parameters.availability)):
        node_info['Spec']['Availability'] = self.parameters.availability
        changed = True
    if (self.parameters.labels_state == 'replace'):
        if (self.parameters.labels is None):
            node_spec['Labels'] = {
                
            }
            if node_info['Spec']['Labels']:
                changed = True
        elif ((node_info['Spec']['Labels'] or {
            
        }) != self.parameters.labels):
            node_spec['Labels'] = self.parameters.labels
            changed = True
    elif (self.parameters.labels_state == 'merge'):
        node_spec['Labels'] = dict((node_info['Spec']['Labels'] or {
            
        }))
        if (self.parameters.labels is not None):
            for (key, value) in self.parameters.labels.items():
                if (node_spec['Labels'].get(key) != value):
                    node_spec['Labels'][key] = value
                    changed = True
        if (self.parameters.labels_to_remove is not None):
            for key in self.parameters.labels_to_remove:
                if (not self.parameters.labels.get(key)):
                    if node_spec['Labels'].get(key):
                        node_spec['Labels'].pop(key)
                        changed = True
                else:
                    self.client.module.warn(("Label '%s' listed both in 'labels' and 'labels_to_remove'. Keeping the assigned label value." % to_native(key)))
    if (changed is True):
        if (not self.check_mode):
            try:
                self.client.update_node(node_id=node_info['ID'], version=node_info['Version']['Index'], node_spec=node_spec)
            except APIError as exc:
                self.client.fail(('Failed to update node : %s' % to_native(exc)))
        self.results['node_facts'] = self.client.get_node_inspect(node_id=node_info['ID'])
        self.results['changed'] = changed
    else:
        self.results['node_facts'] = node_info
        self.results['changed'] = changed
