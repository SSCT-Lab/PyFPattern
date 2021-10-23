def main():
    argument_spec = ovirt_facts_full_argument_spec(pattern=dict(default='', required=False), all_content=dict(default=False, type='bool'), cluster_version=dict(default=None, type='str'))
    module = AnsibleModule(argument_spec)
    check_sdk(module)
    try:
        auth = module.params.pop('auth')
        connection = create_connection(auth)
        hosts_service = connection.system_service().hosts_service()
        hosts = hosts_service.list(search=module.params['pattern'], all_content=module.params['all_content'], follow='cluster')
        cluster_version = module.params.get('cluster_version')
        if (cluster_version is not None):
            hosts = get_filtered_hosts(cluster_version, hosts)
        module.exit_json(changed=False, ansible_facts=dict(ovirt_hosts=[get_dict_of_struct(struct=c, connection=connection, fetch_nested=module.params.get('fetch_nested'), attributes=module.params.get('nested_attributes')) for c in hosts]))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())
    finally:
        connection.close(logout=(auth.get('token') is None))