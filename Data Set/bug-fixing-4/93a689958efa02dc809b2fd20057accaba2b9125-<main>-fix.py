def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(distribution_id=dict(required=False, type='str'), invalidation_id=dict(required=False, type='str'), origin_access_identity_id=dict(required=False, type='str'), domain_name_alias=dict(required=False, type='str'), all_lists=dict(required=False, default=False, type='bool'), distribution=dict(required=False, default=False, type='bool'), distribution_config=dict(required=False, default=False, type='bool'), origin_access_identity=dict(required=False, default=False, type='bool'), origin_access_identity_config=dict(required=False, default=False, type='bool'), invalidation=dict(required=False, default=False, type='bool'), streaming_distribution=dict(required=False, default=False, type='bool'), streaming_distribution_config=dict(required=False, default=False, type='bool'), list_origin_access_identities=dict(required=False, default=False, type='bool'), list_distributions=dict(required=False, default=False, type='bool'), list_distributions_by_web_acl_id=dict(required=False, default=False, type='bool'), list_invalidations=dict(required=False, default=False, type='bool'), list_streaming_distributions=dict(required=False, default=False, type='bool'), summary=dict(required=False, default=False, type='bool')))
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
    summary = module.params.get('summary')
    aliases = []
    result = {
        'cloudfront': {
            
        },
    }
    facts = {
        
    }
    require_distribution_id = (distribution or distribution_config or invalidation or streaming_distribution or streaming_distribution_config or list_invalidations)
    summary = (summary or (not (distribution or distribution_config or origin_access_identity or origin_access_identity_config or invalidation or streaming_distribution or streaming_distribution_config or list_origin_access_identities or list_distributions_by_web_acl_id or list_invalidations or list_streaming_distributions or list_distributions)))
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
        facts = {
            distribution_id: {
                
            },
        }
        aliases = service_mgr.get_aliases_from_distribution_id(distribution_id)
        for alias in aliases:
            facts.update({
                alias: {
                    
                },
            })
        if invalidation_id:
            facts.update({
                invalidation_id: {
                    
                },
            })
    elif (distribution_id and list_invalidations):
        facts = {
            distribution_id: {
                
            },
        }
        aliases = service_mgr.get_aliases_from_distribution_id(distribution_id)
        for alias in aliases:
            facts.update({
                alias: {
                    
                },
            })
    elif origin_access_identity_id:
        facts = {
            origin_access_identity_id: {
                
            },
        }
    elif web_acl_id:
        facts = {
            web_acl_id: {
                
            },
        }
    if distribution:
        facts_to_set = service_mgr.get_distribution(distribution_id)
    if distribution_config:
        facts_to_set = service_mgr.get_distribution_config(distribution_id)
    if origin_access_identity:
        facts[origin_access_identity_id].update(service_mgr.get_origin_access_identity(origin_access_identity_id))
    if origin_access_identity_config:
        facts[origin_access_identity_id].update(service_mgr.get_origin_access_identity_config(origin_access_identity_id))
    if invalidation:
        facts_to_set = service_mgr.get_invalidation(distribution_id, invalidation_id)
        facts[invalidation_id].update(facts_to_set)
    if streaming_distribution:
        facts_to_set = service_mgr.get_streaming_distribution(distribution_id)
    if streaming_distribution_config:
        facts_to_set = service_mgr.get_streaming_distribution_config(distribution_id)
    if list_invalidations:
        facts_to_set = {
            'invalidations': service_mgr.list_invalidations(distribution_id),
        }
    if ('facts_to_set' in vars()):
        facts = set_facts_for_distribution_id_and_alias(facts_to_set, facts, distribution_id, aliases)
    if (all_lists or list_origin_access_identities):
        facts['origin_access_identities'] = service_mgr.list_origin_access_identities()
    if (all_lists or list_distributions):
        facts['distributions'] = service_mgr.list_distributions()
    if (all_lists or list_streaming_distributions):
        facts['streaming_distributions'] = service_mgr.list_streaming_distributions()
    if list_distributions_by_web_acl_id:
        facts['distributions_by_web_acl_id'] = service_mgr.list_distributions_by_web_acl_id(web_acl_id)
    if list_invalidations:
        facts['invalidations'] = service_mgr.list_invalidations(distribution_id)
    if summary:
        facts['summary'] = service_mgr.summary()
    result['changed'] = False
    result['cloudfront'].update(facts)
    module.exit_json(msg='Retrieved cloudfront facts.', ansible_facts=result)