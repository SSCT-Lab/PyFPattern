def get_project_config(project_id, full_config=True, for_store=False):
    '\n    Constructs the ProjectConfig information.\n\n    :param project_id: the project id as int or string\n    :param full_config: True if only the full config is required, False\n        if only the restricted (for external relays) is required\n        (default True, i.e. full configuration)\n    :param for_store: If set to true, this omits all parameters that are not\n        needed for store normalization. This is a temporary flag that should\n        be removed once store has been moved to Relay. Most importantly, this\n        avoids database accesses.\n\n    :return: a ProjectConfig object for the given project\n    '
    project = _get_project_from_id(six.text_type(project_id))
    if (project is None):
        raise APIError('Invalid project id:{}'.format(project_id))
    with configure_scope() as scope:
        scope.set_tag('project', project.id)
    if for_store:
        project_keys = []
    else:
        project_keys = ProjectKey.objects.filter(project=project).all()
    public_keys = {
        
    }
    for project_key in project_keys:
        public_keys[project_key.public_key] = (project_key.status == 0)
    now = datetime.utcnow().replace(tzinfo=utc)
    org_options = OrganizationOption.objects.get_all_values(project.organization_id)
    cfg = {
        'disabled': (project.status > 0),
        'slug': project.slug,
        'lastFetch': now,
        'lastChange': project.get_option('sentry:relay-rev-lastchange', now),
        'rev': project.get_option('sentry:relay-rev', uuid.uuid4().hex),
        'publicKeys': public_keys,
        'config': {
            'allowedDomains': project.get_option('sentry:origins', ['*']),
            'trustedRelays': org_options.get('sentry:trusted-relays', []),
            'piiConfig': _get_pii_config(project, org_options),
        },
        'project_id': project.id,
    }
    if (not full_config):
        return ProjectConfig(project, **cfg)
    cfg['organization_id'] = project.organization_id
    project.organization = Organization.objects.get_from_cache(id=project.organization_id)
    if (project.organization is not None):
        org_options = OrganizationOption.objects.get_all_values(project.organization_id)
    else:
        org_options = {
            
        }
    project_cfg = cfg['config']
    invalid_releases = project.get_option('sentry:{}'.format(FilterTypes.RELEASES))
    if (invalid_releases is not None):
        project_cfg[FilterTypes.RELEASES] = invalid_releases
    blacklisted_ips = project.get_option('sentry:blacklisted_ips')
    if (blacklisted_ips is not None):
        project_cfg['blacklisted_ips'] = blacklisted_ips
    error_messages = project.get_option('sentry:{}'.format(FilterTypes.ERROR_MESSAGES))
    if (error_messages is not None):
        project_cfg[FilterTypes.ERROR_MESSAGES] = error_messages
    filter_settings = {
        
    }
    project_cfg['filter_settings'] = filter_settings
    for flt in get_all_filters():
        filter_id = flt.spec.id
        settings = _load_filter_settings(flt, project)
        filter_settings[filter_id] = settings
    scrub_ip_address = (org_options.get('sentry:require_scrub_ip_address', False) or project.get_option('sentry:scrub_ip_address', False))
    project_cfg['scrub_ip_addresses'] = scrub_ip_address
    scrub_data = (org_options.get('sentry:require_scrub_data', False) or project.get_option('sentry:scrub_data', True))
    project_cfg['scrub_data'] = scrub_data
    project_cfg['grouping_config'] = get_grouping_config_dict_for_project(project)
    project_cfg['allowed_domains'] = list(get_origins(project))
    if scrub_data:
        sensitive_fields_key = 'sentry:sensitive_fields'
        sensitive_fields = (org_options.get(sensitive_fields_key, []) + project.get_option(sensitive_fields_key, []))
        project_cfg['sensitive_fields'] = sensitive_fields
        exclude_fields_key = 'sentry:safe_fields'
        exclude_fields = (org_options.get(exclude_fields_key, []) + project.get_option(exclude_fields_key, []))
        project_cfg['exclude_fields'] = exclude_fields
        scrub_defaults = (org_options.get('sentry:require_scrub_defaults', False) or project.get_option('sentry:scrub_defaults', True))
        project_cfg['scrub_defaults'] = scrub_defaults
    return ProjectConfig(project, **cfg)