def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(required=True, choices=['present', 'absent']), name=dict(), cert=dict(), key=dict(no_log=True), cert_chain=dict(), new_name=dict(), path=dict(default='/', required=False), new_path=dict(required=False), dup_ok=dict(required=False, type='bool')))
    module = AnsibleModule(argument_spec=argument_spec, mutually_exclusive=[['new_path', 'key'], ['new_path', 'cert'], ['new_path', 'cert_chain'], ['new_name', 'key'], ['new_name', 'cert'], ['new_name', 'cert_chain']])
    if (not HAS_BOTO):
        module.fail_json(msg='Boto is required for this module')
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    try:
        if region:
            iam = connect_to_aws(boto.iam, region, **aws_connect_kwargs)
        else:
            iam = boto.iam.connection.IAMConnection(**aws_connect_kwargs)
    except boto.exception.NoAuthHandlerFound as e:
        module.fail_json(msg=str(e))
    state = module.params.get('state')
    name = module.params.get('name')
    path = module.params.get('path')
    new_name = module.params.get('new_name')
    new_path = module.params.get('new_path')
    dup_ok = module.params.get('dup_ok')
    if ((state == 'present') and (not new_name) and (not new_path)):
        cert = module.params.get('cert')
        key = module.params.get('key')
        cert_chain = module.params.get('cert_chain')
    else:
        cert = key = cert_chain = None
    orig_cert_names = [ctb['server_certificate_name'] for ctb in iam.get_all_server_certs().list_server_certificates_result.server_certificate_metadata_list]
    orig_cert_bodies = [iam.get_server_certificate(thing).get_server_certificate_result.certificate_body for thing in orig_cert_names]
    if (new_name == name):
        new_name = None
    if (new_path == path):
        new_path = None
    changed = False
    try:
        cert_action(module, iam, name, path, new_name, new_path, state, cert, key, cert_chain, orig_cert_names, orig_cert_bodies, dup_ok)
    except boto.exception.BotoServerError as err:
        module.fail_json(changed=changed, msg=str(err), debug=[cert, key])