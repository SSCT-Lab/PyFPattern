def main():
    '\n    Module execution\n\n    :return:\n    '
    argument_spec = keycloak_argument_spec()
    protmapper_spec = dict(consentRequired=dict(type='bool'), consentText=dict(type='str'), id=dict(type='str'), name=dict(type='str'), protocol=dict(type='str', choices=['openid-connect', 'saml']), protocolMapper=dict(type='str'), config=dict(type='dict'))
    meta_args = dict(state=dict(default='present', choices=['present', 'absent']), realm=dict(type='str', default='master'), id=dict(type='str'), client_id=dict(type='str', aliases=['clientId']), name=dict(type='str'), description=dict(type='str'), root_url=dict(type='str', aliases=['rootUrl']), admin_url=dict(type='str', aliases=['adminUrl']), base_url=dict(type='str', aliases=['baseUrl']), surrogate_auth_required=dict(type='bool', aliases=['surrogateAuthRequired']), enabled=dict(type='bool'), client_authenticator_type=dict(type='str', choices=['client-secret', 'client-jwt'], aliases=['clientAuthenticatorType']), secret=dict(type='str', no_log=True), registration_access_token=dict(type='str', aliases=['registrationAccessToken']), default_roles=dict(type='list', aliases=['defaultRoles']), redirect_uris=dict(type='list', aliases=['redirectUris']), web_origins=dict(type='list', aliases=['webOrigins']), not_before=dict(type='int', aliases=['notBefore']), bearer_only=dict(type='bool', aliases=['bearerOnly']), consent_required=dict(type='bool', aliases=['consentRequired']), standard_flow_enabled=dict(type='bool', aliases=['standardFlowEnabled']), implicit_flow_enabled=dict(type='bool', aliases=['implicitFlowEnabled']), direct_access_grants_enabled=dict(type='bool', aliases=['directAccessGrantsEnabled']), service_accounts_enabled=dict(type='bool', aliases=['serviceAccountsEnabled']), authorization_services_enabled=dict(type='bool', aliases=['authorizationServicesEnabled']), public_client=dict(type='bool', aliases=['publicClient']), frontchannel_logout=dict(type='bool', aliases=['frontchannelLogout']), protocol=dict(type='str', choices=['openid-connect', 'saml']), attributes=dict(type='dict'), full_scope_allowed=dict(type='bool', aliases=['fullScopeAllowed']), node_re_registration_timeout=dict(type='int', aliases=['nodeReRegistrationTimeout']), registered_nodes=dict(type='dict', aliases=['registeredNodes']), client_template=dict(type='str', aliases=['clientTemplate']), use_template_config=dict(type='bool', aliases=['useTemplateConfig']), use_template_scope=dict(type='bool', aliases=['useTemplateScope']), use_template_mappers=dict(type='bool', aliases=['useTemplateMappers']), protocol_mappers=dict(type='list', elements='dict', options=protmapper_spec, aliases=['protocolMappers']), authorization_settings=dict(type='dict', aliases=['authorizationSettings']))
    argument_spec.update(meta_args)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['client_id', 'id']])
    result = dict(changed=False, msg='', diff={
        
    }, proposed={
        
    }, existing={
        
    }, end_state={
        
    })
    kc = KeycloakAPI(module)
    realm = module.params.get('realm')
    cid = module.params.get('id')
    state = module.params.get('state')
    client_params = [x for x in module.params if ((x not in (list(keycloak_argument_spec().keys()) + ['state', 'realm'])) and (module.params.get(x) is not None))]
    keycloak_argument_spec().keys()
    if (cid is None):
        before_client = kc.get_client_by_clientid(module.params.get('client_id'), realm=realm)
        if (before_client is not None):
            cid = before_client['id']
    else:
        before_client = kc.get_client_by_id(cid, realm=realm)
    if (before_client is None):
        before_client = dict()
    changeset = dict()
    for client_param in client_params:
        new_param_value = module.params.get(client_param)
        if isinstance(new_param_value, list):
            if (client_param in ['attributes']):
                try:
                    new_param_value = sorted(new_param_value)
                except TypeError:
                    pass
        if (client_param == 'protocol_mappers'):
            new_param_value = [dict(((k, v) for (k, v) in x.items() if (x[k] is not None))) for x in new_param_value]
        changeset[camel(client_param)] = new_param_value
    updated_client = before_client.copy()
    updated_client.update(changeset)
    result['proposed'] = sanitize_cr(changeset)
    result['existing'] = sanitize_cr(before_client)
    if (before_client == dict()):
        if (state == 'absent'):
            if module._diff:
                result['diff'] = dict(before='', after='')
            result['msg'] = 'Client does not exist, doing nothing.'
            module.exit_json(**result)
        result['changed'] = True
        if ('clientId' not in updated_client):
            module.fail_json(msg='client_id needs to be specified when creating a new client')
        if module._diff:
            result['diff'] = dict(before='', after=sanitize_cr(updated_client))
        if module.check_mode:
            module.exit_json(**result)
        kc.create_client(updated_client, realm=realm)
        after_client = kc.get_client_by_clientid(updated_client['clientId'], realm=realm)
        result['end_state'] = sanitize_cr(after_client)
        result['msg'] = ('Client %s has been created.' % updated_client['clientId'])
        module.exit_json(**result)
    elif (state == 'present'):
        result['changed'] = True
        if module.check_mode:
            if module._diff:
                result['diff'] = dict(before=sanitize_cr(before_client), after=sanitize_cr(updated_client))
            module.exit_json(**result)
        kc.update_client(cid, updated_client, realm=realm)
        after_client = kc.get_client_by_id(cid, realm=realm)
        if (before_client == after_client):
            result['changed'] = False
        if module._diff:
            result['diff'] = dict(before=sanitize_cr(before_client), after=sanitize_cr(after_client))
        result['end_state'] = sanitize_cr(after_client)
        result['msg'] = ('Client %s has been updated.' % updated_client['clientId'])
        module.exit_json(**result)
    else:
        result['changed'] = True
        if module._diff:
            result['diff']['before'] = sanitize_cr(before_client)
            result['diff']['after'] = ''
        if module.check_mode:
            module.exit_json(**result)
        kc.delete_client(cid, realm=realm)
        result['proposed'] = dict()
        result['end_state'] = dict()
        result['msg'] = ('Client %s has been deleted.' % before_client['clientId'])
        module.exit_json(**result)
    module.exit_json(**result)