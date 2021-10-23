def read_settings(self):
    ' Reads the settings from the ec2.ini file '
    scriptbasename = __file__
    scriptbasename = os.path.basename(scriptbasename)
    scriptbasename = scriptbasename.replace('.py', '')
    defaults = {
        'ec2': {
            'ini_fallback': os.path.join(os.path.dirname(__file__), 'ec2.ini'),
            'ini_path': os.path.join(os.path.dirname(__file__), ('%s.ini' % scriptbasename)),
        },
    }
    if six.PY3:
        config = configparser.ConfigParser(DEFAULTS)
    else:
        config = configparser.SafeConfigParser(DEFAULTS)
    ec2_ini_path = os.environ.get('EC2_INI_PATH', defaults['ec2']['ini_path'])
    ec2_ini_path = os.path.expanduser(os.path.expandvars(ec2_ini_path))
    if (not os.path.isfile(ec2_ini_path)):
        ec2_ini_path = os.path.expanduser(defaults['ec2']['ini_fallback'])
    if os.path.isfile(ec2_ini_path):
        config.read(ec2_ini_path)
    try:
        config.add_section('ec2')
    except configparser.DuplicateSectionError:
        pass
    try:
        config.add_section('credentials')
    except configparser.DuplicateSectionError:
        pass
    self.eucalyptus = config.getboolean('ec2', 'eucalyptus')
    self.eucalyptus_host = config.get('ec2', 'eucalyptus_host')
    self.regions = []
    configRegions = config.get('ec2', 'regions')
    if (configRegions == 'all'):
        if self.eucalyptus_host:
            self.regions.append(boto.connect_euca(host=self.eucalyptus_host).region.name, **self.credentials)
        else:
            configRegions_exclude = config.get('ec2', 'regions_exclude')
            for regionInfo in ec2.regions():
                if (regionInfo.name not in configRegions_exclude):
                    self.regions.append(regionInfo.name)
    else:
        self.regions = configRegions.split(',')
    if ('auto' in self.regions):
        env_region = os.environ.get('AWS_REGION')
        if (env_region is None):
            env_region = os.environ.get('AWS_DEFAULT_REGION')
        self.regions = [env_region]
    self.destination_variable = config.get('ec2', 'destination_variable')
    self.vpc_destination_variable = config.get('ec2', 'vpc_destination_variable')
    self.hostname_variable = config.get('ec2', 'hostname_variable')
    if (config.has_option('ec2', 'destination_format') and config.has_option('ec2', 'destination_format_tags')):
        self.destination_format = config.get('ec2', 'destination_format')
        self.destination_format_tags = config.get('ec2', 'destination_format_tags').split(',')
    else:
        self.destination_format = None
        self.destination_format_tags = None
    self.route53_enabled = config.getboolean('ec2', 'route53')
    self.route53_hostnames = config.get('ec2', 'route53_hostnames')
    self.route53_excluded_zones = []
    self.route53_excluded_zones = [a for a in config.get('ec2', 'route53_excluded_zones').split(',') if a]
    self.rds_enabled = config.getboolean('ec2', 'rds')
    self.include_rds_clusters = config.getboolean('ec2', 'include_rds_clusters')
    self.elasticache_enabled = config.getboolean('ec2', 'elasticache')
    self.all_instances = config.getboolean('ec2', 'all_instances')
    ec2_valid_instance_states = ['pending', 'running', 'shutting-down', 'terminated', 'stopping', 'stopped']
    self.ec2_instance_states = []
    if self.all_instances:
        self.ec2_instance_states = ec2_valid_instance_states
    elif config.has_option('ec2', 'instance_states'):
        for instance_state in config.get('ec2', 'instance_states').split(','):
            instance_state = instance_state.strip()
            if (instance_state not in ec2_valid_instance_states):
                continue
            self.ec2_instance_states.append(instance_state)
    else:
        self.ec2_instance_states = ['running']
    self.all_rds_instances = config.getboolean('ec2', 'all_rds_instances')
    self.all_elasticache_replication_groups = config.getboolean('ec2', 'all_elasticache_replication_groups')
    self.all_elasticache_clusters = config.getboolean('ec2', 'all_elasticache_clusters')
    self.all_elasticache_nodes = config.getboolean('ec2', 'all_elasticache_nodes')
    self.boto_profile = (self.args.boto_profile or os.environ.get('AWS_PROFILE') or config.get('ec2', 'boto_profile'))
    if (not (self.boto_profile or os.environ.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_PROFILE'))):
        aws_access_key_id = config.get('credentials', 'aws_access_key_id')
        aws_secret_access_key = config.get('credentials', 'aws_secret_access_key')
        aws_security_token = config.get('credentials', 'aws_security_token')
        if aws_access_key_id:
            self.credentials = {
                'aws_access_key_id': aws_access_key_id,
                'aws_secret_access_key': aws_secret_access_key,
            }
            if aws_security_token:
                self.credentials['security_token'] = aws_security_token
    cache_dir = os.path.expanduser(config.get('ec2', 'cache_path'))
    if self.boto_profile:
        cache_dir = os.path.join(cache_dir, ('profile_' + self.boto_profile))
    if (not os.path.exists(cache_dir)):
        os.makedirs(cache_dir)
    cache_name = 'ansible-ec2'
    cache_id = (self.boto_profile or os.environ.get('AWS_ACCESS_KEY_ID', self.credentials.get('aws_access_key_id')))
    if cache_id:
        cache_name = ('%s-%s' % (cache_name, cache_id))
    cache_name += ('-' + str(abs(hash(__file__)))[1:7])
    self.cache_path_cache = os.path.join(cache_dir, ('%s.cache' % cache_name))
    self.cache_path_index = os.path.join(cache_dir, ('%s.index' % cache_name))
    self.cache_max_age = config.getint('ec2', 'cache_max_age')
    self.expand_csv_tags = config.getboolean('ec2', 'expand_csv_tags')
    self.nested_groups = config.getboolean('ec2', 'nested_groups')
    self.replace_dash_in_groups = config.getboolean('ec2', 'replace_dash_in_groups')
    self.iam_role = config.get('ec2', 'iam_role')
    group_by_options = [a for a in DEFAULTS if a.startswith('group_by')]
    for option in group_by_options:
        setattr(self, option, config.getboolean('ec2', option))
    self.pattern_include = config.get('ec2', 'pattern_include')
    if self.pattern_include:
        self.pattern_include = re.compile(self.pattern_include)
    self.pattern_exclude = config.get('ec2', 'pattern_exclude')
    if self.pattern_exclude:
        self.pattern_exclude = re.compile(self.pattern_exclude)
    self.stack_filters = config.getboolean('ec2', 'stack_filters')
    self.ec2_instance_filters = []
    if config.has_option('ec2', 'instance_filters'):
        filters = config.get('ec2', 'instance_filters')
        if (self.stack_filters and ('&' in filters)):
            self.fail_with_error('AND filters along with stack_filter enabled is not supported.\n')
        filter_sets = [f for f in filters.split(',') if f]
        for filter_set in filter_sets:
            filters = {
                
            }
            filter_set = filter_set.strip()
            for instance_filter in filter_set.split('&'):
                instance_filter = instance_filter.strip()
                if ((not instance_filter) or ('=' not in instance_filter)):
                    continue
                (filter_key, filter_value) = [x.strip() for x in instance_filter.split('=', 1)]
                if (not filter_key):
                    continue
                filters[filter_key] = filter_value
            self.ec2_instance_filters.append(filters.copy())