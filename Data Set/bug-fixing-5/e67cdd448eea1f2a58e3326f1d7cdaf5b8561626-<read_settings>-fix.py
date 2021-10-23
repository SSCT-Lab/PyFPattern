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
        config = configparser.ConfigParser()
    else:
        config = configparser.SafeConfigParser()
    ec2_ini_path = os.environ.get('EC2_INI_PATH', defaults['ec2']['ini_path'])
    ec2_ini_path = os.path.expanduser(os.path.expandvars(ec2_ini_path))
    if (not os.path.isfile(ec2_ini_path)):
        ec2_ini_path = os.path.expanduser(defaults['ec2']['ini_fallback'])
    config.read(ec2_ini_path)
    self.eucalyptus_host = None
    self.eucalyptus = False
    if config.has_option('ec2', 'eucalyptus'):
        self.eucalyptus = config.getboolean('ec2', 'eucalyptus')
    if (self.eucalyptus and config.has_option('ec2', 'eucalyptus_host')):
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
    if config.has_option('ec2', 'hostname_variable'):
        self.hostname_variable = config.get('ec2', 'hostname_variable')
    else:
        self.hostname_variable = None
    if (config.has_option('ec2', 'destination_format') and config.has_option('ec2', 'destination_format_tags')):
        self.destination_format = config.get('ec2', 'destination_format')
        self.destination_format_tags = config.get('ec2', 'destination_format_tags').split(',')
    else:
        self.destination_format = None
        self.destination_format_tags = None
    self.route53_enabled = config.getboolean('ec2', 'route53')
    if config.has_option('ec2', 'route53_hostnames'):
        self.route53_hostnames = config.get('ec2', 'route53_hostnames')
    else:
        self.route53_hostnames = None
    self.route53_excluded_zones = []
    if config.has_option('ec2', 'route53_excluded_zones'):
        self.route53_excluded_zones.extend(config.get('ec2', 'route53_excluded_zones', '').split(','))
    self.rds_enabled = True
    if config.has_option('ec2', 'rds'):
        self.rds_enabled = config.getboolean('ec2', 'rds')
    if config.has_option('ec2', 'include_rds_clusters'):
        self.include_rds_clusters = config.getboolean('ec2', 'include_rds_clusters')
    else:
        self.include_rds_clusters = False
    self.elasticache_enabled = True
    if config.has_option('ec2', 'elasticache'):
        self.elasticache_enabled = config.getboolean('ec2', 'elasticache')
    if config.has_option('ec2', 'all_instances'):
        self.all_instances = config.getboolean('ec2', 'all_instances')
    else:
        self.all_instances = False
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
    if (config.has_option('ec2', 'all_rds_instances') and self.rds_enabled):
        self.all_rds_instances = config.getboolean('ec2', 'all_rds_instances')
    else:
        self.all_rds_instances = False
    if (config.has_option('ec2', 'all_elasticache_replication_groups') and self.elasticache_enabled):
        self.all_elasticache_replication_groups = config.getboolean('ec2', 'all_elasticache_replication_groups')
    else:
        self.all_elasticache_replication_groups = False
    if (config.has_option('ec2', 'all_elasticache_clusters') and self.elasticache_enabled):
        self.all_elasticache_clusters = config.getboolean('ec2', 'all_elasticache_clusters')
    else:
        self.all_elasticache_clusters = False
    if (config.has_option('ec2', 'all_elasticache_nodes') and self.elasticache_enabled):
        self.all_elasticache_nodes = config.getboolean('ec2', 'all_elasticache_nodes')
    else:
        self.all_elasticache_nodes = False
    self.boto_profile = (self.args.boto_profile or os.environ.get('AWS_PROFILE'))
    if (config.has_option('ec2', 'boto_profile') and (not self.boto_profile)):
        self.boto_profile = config.get('ec2', 'boto_profile')
    if (not (self.boto_profile or os.environ.get('AWS_ACCESS_KEY_ID') or os.environ.get('AWS_PROFILE'))):
        if config.has_option('credentials', 'aws_access_key_id'):
            aws_access_key_id = config.get('credentials', 'aws_access_key_id')
        else:
            aws_access_key_id = None
        if config.has_option('credentials', 'aws_secret_access_key'):
            aws_secret_access_key = config.get('credentials', 'aws_secret_access_key')
        else:
            aws_secret_access_key = None
        if config.has_option('credentials', 'aws_security_token'):
            aws_security_token = config.get('credentials', 'aws_security_token')
        else:
            aws_security_token = None
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
    self.cache_path_cache = os.path.join(cache_dir, ('%s.cache' % cache_name))
    self.cache_path_index = os.path.join(cache_dir, ('%s.index' % cache_name))
    self.cache_max_age = config.getint('ec2', 'cache_max_age')
    if config.has_option('ec2', 'expand_csv_tags'):
        self.expand_csv_tags = config.getboolean('ec2', 'expand_csv_tags')
    else:
        self.expand_csv_tags = False
    if config.has_option('ec2', 'nested_groups'):
        self.nested_groups = config.getboolean('ec2', 'nested_groups')
    else:
        self.nested_groups = False
    if config.has_option('ec2', 'replace_dash_in_groups'):
        self.replace_dash_in_groups = config.getboolean('ec2', 'replace_dash_in_groups')
    else:
        self.replace_dash_in_groups = True
    if config.has_option('ec2', 'iam_role'):
        self.iam_role = config.get('ec2', 'iam_role')
    else:
        self.iam_role = None
    group_by_options = ['group_by_instance_id', 'group_by_region', 'group_by_availability_zone', 'group_by_ami_id', 'group_by_instance_type', 'group_by_instance_state', 'group_by_key_pair', 'group_by_vpc_id', 'group_by_security_group', 'group_by_tag_keys', 'group_by_tag_none', 'group_by_route53_names', 'group_by_rds_engine', 'group_by_rds_parameter_group', 'group_by_elasticache_engine', 'group_by_elasticache_cluster', 'group_by_elasticache_parameter_group', 'group_by_elasticache_replication_group', 'group_by_aws_account']
    for option in group_by_options:
        if config.has_option('ec2', option):
            setattr(self, option, config.getboolean('ec2', option))
        else:
            setattr(self, option, True)
    try:
        pattern_include = config.get('ec2', 'pattern_include')
        if (pattern_include and (len(pattern_include) > 0)):
            self.pattern_include = re.compile(pattern_include)
        else:
            self.pattern_include = None
    except configparser.NoOptionError:
        self.pattern_include = None
    try:
        pattern_exclude = config.get('ec2', 'pattern_exclude')
        if (pattern_exclude and (len(pattern_exclude) > 0)):
            self.pattern_exclude = re.compile(pattern_exclude)
        else:
            self.pattern_exclude = None
    except configparser.NoOptionError:
        self.pattern_exclude = None
    if config.has_option('ec2', 'stack_filters'):
        self.stack_filters = config.getboolean('ec2', 'stack_filters')
    else:
        self.stack_filters = False
    self.ec2_instance_filters = defaultdict(list)
    if config.has_option('ec2', 'instance_filters'):
        filters = [f for f in config.get('ec2', 'instance_filters').split(',') if f]
        for instance_filter in filters:
            instance_filter = instance_filter.strip()
            if ((not instance_filter) or ('=' not in instance_filter)):
                continue
            (filter_key, filter_value) = [x.strip() for x in instance_filter.split('=', 1)]
            if (not filter_key):
                continue
            self.ec2_instance_filters[filter_key].append(filter_value)