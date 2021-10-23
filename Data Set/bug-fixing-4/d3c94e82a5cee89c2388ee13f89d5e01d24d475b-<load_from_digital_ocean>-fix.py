def load_from_digital_ocean(self, resource=None):
    'Get JSON from DigitalOcean API'
    if (self.args.force_cache and os.path.isfile(self.cache_filename)):
        return
    if (self.is_cache_valid() and (not ((resource == 'droplets') or (resource is None)))):
        return
    if self.args.refresh_cache:
        resource = None
    if ((resource == 'droplets') or (resource is None)):
        self.data['droplets'] = self.manager.all_active_droplets()
        self.cache_refreshed = True
    if ((resource == 'regions') or (resource is None)):
        self.data['regions'] = self.manager.all_regions()
        self.cache_refreshed = True
    if ((resource == 'images') or (resource is None)):
        self.data['images'] = self.manager.all_images(filter=None)
        self.cache_refreshed = True
    if ((resource == 'sizes') or (resource is None)):
        self.data['sizes'] = self.manager.sizes()
        self.cache_refreshed = True
    if ((resource == 'ssh_keys') or (resource is None)):
        self.data['ssh_keys'] = self.manager.all_ssh_keys()
        self.cache_refreshed = True
    if ((resource == 'domains') or (resource is None)):
        self.data['domains'] = self.manager.all_domains()
        self.cache_refreshed = True