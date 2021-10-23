def build_inventory(self):
    ' Build Ansible inventory of droplets '
    self.inventory = {
        'all': {
            'hosts': [],
            'vars': self.group_variables,
        },
        '_meta': {
            'hostvars': {
                
            },
        },
    }
    for droplet in self.data['droplets']:
        for net in droplet['networks']['v4']:
            if (net['type'] == 'public'):
                dest = net['ip_address']
            else:
                continue
        self.inventory['all']['hosts'].append(dest)
        self.add_host(droplet['id'], dest)
        self.add_host(droplet['name'], dest)
        for group in ('digital_ocean', ('region_' + droplet['region']['slug']), ('image_' + str(droplet['image']['id'])), ('size_' + droplet['size']['slug']), ('distro_' + DigitalOceanInventory.to_safe(droplet['image']['distribution'])), ('status_' + droplet['status'])):
            self.add_host(group, dest)
        for group in (droplet['image']['slug'], droplet['image']['name']):
            if group:
                image = ('image_' + DigitalOceanInventory.to_safe(group))
                self.add_host(image, dest)
        if droplet['tags']:
            for tag in droplet['tags']:
                self.add_host(tag, dest)
        info = self.do_namespace(droplet)
        self.inventory['_meta']['hostvars'][dest] = info