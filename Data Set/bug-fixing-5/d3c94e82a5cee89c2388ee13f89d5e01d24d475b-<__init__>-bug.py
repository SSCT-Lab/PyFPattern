def __init__(self):
    ' Main execution path '
    self.data = {
        
    }
    self.inventory = {
        
    }
    self.cache_path = '.'
    self.cache_max_age = 0
    self.use_private_network = False
    self.group_variables = {
        
    }
    self.read_settings()
    self.read_environment()
    self.read_cli_args()
    if (not hasattr(self, 'api_token')):
        sys.stderr.write('Could not find values for DigitalOcean api_token.\nThey must be specified via either ini file, command line argument (--api-token),\nor environment variables (DO_API_TOKEN)\n')
        sys.exit((- 1))
    if self.args.env:
        print(('DO_API_TOKEN=%s' % self.api_token))
        sys.exit(0)
    self.cache_filename = (self.cache_path + '/ansible-digital_ocean.cache')
    self.cache_refreshed = False
    if self.is_cache_valid:
        self.load_from_cache()
        if (len(self.data) == 0):
            if self.args.force_cache:
                sys.stderr.write('Cache is empty and --force-cache was specified\n')
                sys.exit((- 1))
    self.manager = DoManager(None, self.api_token, api_version=2)
    if self.args.droplets:
        self.load_from_digital_ocean('droplets')
        json_data = {
            'droplets': self.data['droplets'],
        }
    elif self.args.regions:
        self.load_from_digital_ocean('regions')
        json_data = {
            'regions': self.data['regions'],
        }
    elif self.args.images:
        self.load_from_digital_ocean('images')
        json_data = {
            'images': self.data['images'],
        }
    elif self.args.sizes:
        self.load_from_digital_ocean('sizes')
        json_data = {
            'sizes': self.data['sizes'],
        }
    elif self.args.ssh_keys:
        self.load_from_digital_ocean('ssh_keys')
        json_data = {
            'ssh_keys': self.data['ssh_keys'],
        }
    elif self.args.domains:
        self.load_from_digital_ocean('domains')
        json_data = {
            'domains': self.data['domains'],
        }
    elif self.args.all:
        self.load_from_digital_ocean()
        json_data = self.data
    elif self.args.host:
        json_data = self.load_droplet_variables_for_host()
    else:
        self.load_from_digital_ocean('droplets')
        self.build_inventory()
        json_data = self.inventory
    if self.cache_refreshed:
        self.write_to_cache()
    if self.args.pretty:
        print(json.dumps(json_data, sort_keys=True, indent=2))
    else:
        print(json.dumps(json_data))