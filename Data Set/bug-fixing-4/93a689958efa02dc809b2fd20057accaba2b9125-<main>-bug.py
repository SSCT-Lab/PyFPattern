def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(distribution_id=dict(required=False, type='str'), invalidation_id=dict(required=False, type='str'), origin_access_identity_id=dict(required=False, type='str'), domain_name_alias=dict(required=False, type='str'), all_lists=dict(required=False, default=False, type='bool'), distribution=dict(required=False, default=False, type='bool'), distribution_config=dict(required=False, default=False, type='bool'), origin_access_identity=dict(required=False, default=False, type='bool'), origin_access_identity_config=dict(required=False, default=False, type='bool'), invalidation=dict(required=False, default=False, type='bool'), streaming_distribution=dict(required=False, default=False, type='bool'), streaming_distribution_config=dict(required=False, default=False, type='bool'), list_origin_access_identities=dict(required=False, default=False, type='bool'), list_distributions=dict(required=False, default=False, type='bool'), list_distributions_by_web_acl_id=dict(required=False, default=False, type='bool'), list_invalidations=dict(required=False, default=False, type='bool'), list_streaming_distributions=dict(required=False, default=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_BOTO3):
        module.fail_json(msg='boto3 is required.')
    service_mgr = CloudFrontServiceManager(module)
    distribution_id = module.params.get('distribution_id')
    invalidation_id = module.params.get('invalidation_id')
    origin_access_identity_id = module.params.get('origin_access_identity_id')
    web_acl_id = module.params.get('web_acl_id')
    domain_name_alias = module.params.get('domain_name_alias')
    all_lists = module.params.get('all_lists')
    distribution = module.params.get('distribution')
    distribution_config = module.params.get('distribution_config')
    origin_access_identity = module.params.get('origin_access_identity')
    origin_access_identity_config = module.params.get('origin_access_identity_config')
    invalidation = module.params.get('invalidation')
    streaming_distribution = module.params.get('streaming_distribution')
    streaming_distribution_config = module.params.get('streaming_distribution_config')
    list_origin_access_identities = module.params.get('list_origin_access_identities')
    list_distributions = module.params.get('list_distributions')
    list_distributions_by_web_acl_id = module.params.get('list_distributions_by_web_acl_id')
    list_invalidations = module.params.get('list_invalidations')
    list_streaming_distributions = module.params.get('list_streaming_distributions')
    aliases = []
    require_distribution_id = (distribution or distribution_config or invalidation or streaming_distribution or streaming_distribution_config or list_invalidations)
    list_distributions = (list_distributions or (not (distribution or distribution_config or origin_access_identity or origin_access_identity_config or invalidation or streaming_distribution or streaming_distribution_config or list_origin_access_identities or list_distributions_by_web_acl_id or list_invalidations or list_streaming_distributions)))
    if (require_distribution_id and (distribution_id is None) and (domain_name_alias is None)):
        module.fail_json(msg='Error distribution_id or domain_name_alias have not been specified.')
    if (invalidation and (invalidation_id is None)):
        module.fail_json(msg='Error invalidation_id has not been specified.')
    if ((origin_access_identity or origin_access_identity_config) and (origin_access_identity_id is None)):
        module.fail_json(msg='Error origin_access_identity_id has not been specified.')
    if (list_distributions_by_web_acl_id and (web_acl_id is None)):
        module.fail_json(msg='Error web_acl_id has not been specified.')
    if (require_distribution_id and (distribution_id is None)):
        distribution_id = service_mgr.get_distribution_id_from_domain_name(domain_name_alias)
        if (not distribution_id):
            module.fail_json(msg='Error unable to source a distribution id from domain_name_alias')
    if (distribution_id and (not list_invalidations)):
        result = {
            'cloudfront': {
                distribution_id: {
                    
                },
            },
        }
        aliases = service_mgr.get_aliases_from_distribution_id(distribution_id)
        for alias in aliases:
            result['cloudfront'].update({
                alias: {
                    
                },
            })
        if invalidation_id:
            result['cloudfront'].update({
                invalidation_id: {
                    
                },
            })
        facts = result['cloudfront']
    elif list_invalidations:
        result = {
            'cloudfront': {
                'invalidations': {
                    
                },
            },
        }
        facts = result['cloudfront']['invalidations']
        aliases = service_mgr.get_aliases_from_distribution_id(distribution_id)
        for alias in aliases:
            result['cloudfront']['invalidations'].update({
                alias: {
                    
                },
            })
    elif origin_access_identity_id:
        result = {
            'cloudfront': {
                origin_access_identity_id: {
                    
                },
            },
        }
        facts = result['cloudfront'][origin_access_identity_id]
    elif web_acl_id:
        result = {
            'cloudfront': {
                web_acl_id: {
                    
                },
            },
        }
        facts = result['cloudfront'][web_acl_id]
    else:
        result = {
            'cloudfront': {
                
            },
        }
        facts = result['cloudfront']
    if distribution:
        distribution_details = service_mgr.get_distribution(distribution_id)
        facts[distribution_id].update(distribution_details)
        for alias in aliases:
            facts[alias].update(distribution_details)
    if distribution_config:
        distribution_config_details = service_mgr.get_distribution_config(distribution_id)
        facts[distribution_id].update(distribution_config_details)
        for alias in aliases:
            facts[alias].update(distribution_config_details)
    if origin_access_identity:
        facts[origin_access_identity_id].update(service_mgr.get_origin_access_identity(origin_access_identity_id))
    if origin_access_identity_config:
        facts[origin_access_identity_id].update(service_mgr.get_origin_access_identity_config(origin_access_identity_id))
    if invalidation:
        invalidation = service_mgr.get_invalidation(distribution_id, invalidation_id)
        facts[invalidation_id].update(invalidation)
        facts[distribution_id].update(invalidation)
        for alias in aliases:
            facts[alias].update(invalidation)
    if streaming_distribution:
        streaming_distribution_details = service_mgr.get_streaming_distribution(distribution_id)
        facts[distribution_id].update(streaming_distribution_details)
        for alias in aliases:
            facts[alias].update(streaming_distribution_details)
    if streaming_distribution_config:
        streaming_distribution_config_details = service_mgr.get_streaming_distribution_config(distribution_id)
        facts[distribution_id].update(streaming_distribution_config_details)
        for alias in aliases:
            facts[alias].update(streaming_distribution_config_details)
    if list_invalidations:
        invalidations = service_mgr.list_invalidations(distribution_id)
        facts[distribution_id].update(invalidations)
        for alias in aliases:
            facts[alias].update(invalidations)
    if (all_lists or list_origin_access_identities):
        facts['origin_access_identities'] = service_mgr.list_origin_access_identities()
    if (all_lists or list_distributions):
        facts['distributions'] = service_mgr.list_distributions()
    if (all_lists or list_streaming_distributions):
        facts['streaming_distributions'] = service_mgr.list_streaming_distributions()
    if list_distributions_by_web_acl_id:
        facts['distributions_by_web_acl_id'] = service_mgr.list_distributions_by_web_acl_id(web_acl_id)
    result['changed'] = False
    module.exit_json(msg='Retrieved cloudfront facts.', ansible_facts=result)