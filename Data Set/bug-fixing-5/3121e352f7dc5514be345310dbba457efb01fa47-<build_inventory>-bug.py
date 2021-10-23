def build_inventory(self):
    'Build Ansible inventory of droplets'
    self.inventory = {
        
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
        dest = {
            'hosts': [dest],
            'vars': self.group_variables,
        }
        self.inventory[droplet['id']] = dest
        self.inventory[droplet['name']] = dest
        self.inventory[('region_' + droplet['region']['slug'])] = dest
        self.inventory[('image_' + str(droplet['image']['id']))] = dest
        self.inventory[('size_' + droplet['size']['slug'])] = dest
        image_slug = droplet['image']['slug']
        if image_slug:
            self.inventory[('image_' + self.to_safe(image_slug))] = dest
        else:
            image_name = droplet['image']['name']
            if image_name:
                self.inventory[('image_' + self.to_safe(image_name))] = dest
        self.inventory[('distro_' + self.to_safe(droplet['image']['distribution']))] = dest
        self.inventory[('status_' + droplet['status'])] = dest