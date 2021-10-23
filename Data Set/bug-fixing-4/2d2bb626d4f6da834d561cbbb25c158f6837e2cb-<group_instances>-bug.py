def group_instances(self, zones=None):
    'Group all instances'
    groups = {
        
    }
    meta = {
        
    }
    meta['hostvars'] = {
        
    }
    for node in self.driver.list_nodes():
        if (self.instance_states and (not (node.extra['status'] in self.instance_states))):
            continue
        name = node.name
        meta['hostvars'][name] = self.node_to_dict(node)
        zone = node.extra['zone'].name
        if (zones and (zone not in zones)):
            continue
        if groups.has_key(zone):
            groups[zone].append(name)
        else:
            groups[zone] = [name]
        tags = node.extra['tags']
        for t in tags:
            if t.startswith('group-'):
                tag = t[6:]
            else:
                tag = ('tag_%s' % t)
            if groups.has_key(tag):
                groups[tag].append(name)
            else:
                groups[tag] = [name]
        net = node.extra['networkInterfaces'][0]['network'].split('/')[(- 1)]
        net = ('network_%s' % net)
        if groups.has_key(net):
            groups[net].append(name)
        else:
            groups[net] = [name]
        machine_type = node.size
        if groups.has_key(machine_type):
            groups[machine_type].append(name)
        else:
            groups[machine_type] = [name]
        image = ((node.image and node.image) or 'persistent_disk')
        if groups.has_key(image):
            groups[image].append(name)
        else:
            groups[image] = [name]
        status = node.extra['status']
        stat = ('status_%s' % status.lower())
        if groups.has_key(stat):
            groups[stat].append(name)
        else:
            groups[stat] = [name]
    groups['_meta'] = meta
    return groups