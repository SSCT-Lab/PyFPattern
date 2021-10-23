

def build_inventory(self):
    'Build Ansible inventory of droplets'
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
        if (('private_networking' in droplet['features']) and (not self.use_private_network)):
            for net in droplet['networks']['v4']:
                if (net['type'] == 'public'):
                    dest = net['ip_address']
                else:
                    continue
        else:
            dest = droplet['ip_address']
        self.inventory['all']['hosts'].append(dest)
        self.inventory[droplet['id']] = [dest]
        self.inventory[droplet['name']] = [dest]
        for group in [('region_' + droplet['region']['slug']), ('image_' + str(droplet['image']['id'])), ('size_' + droplet['size']['slug']), ('distro_' + self.to_safe(droplet['image']['distribution'])), ('status_' + droplet['status'])]:
            if (group not in self.inventory):
                self.inventory[group] = {
                    'hosts': [],
                    'vars': {
                        
                    },
                }
            self.inventory[group]['hosts'].append(dest)
        for group in [droplet['image']['slug'], droplet['image']['name']]:
            if group:
                image = ('image_' + self.to_safe(group))
                if (image not in self.inventory):
                    self.inventory[image] = {
                        'hosts': [],
                        'vars': {
                            
                        },
                    }
                self.inventory[image]['hosts'].append(dest)
