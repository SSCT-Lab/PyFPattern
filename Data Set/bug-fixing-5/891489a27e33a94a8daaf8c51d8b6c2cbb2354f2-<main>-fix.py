def main():
    argument_spec = postgres_common_argument_spec()
    argument_spec.update(name=dict(required=True), db=dict(type='str', aliases=['login_db']), state=dict(type='str', default='present', choices=['absent', 'present']), tables=dict(type='list'), parameters=dict(type='dict'), owner=dict(type='str'), cascade=dict(type='bool', default=False))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    name = module.params['name']
    state = module.params['state']
    tables = module.params['tables']
    params = module.params['parameters']
    owner = module.params['owner']
    cascade = module.params['cascade']
    if (state == 'absent'):
        if tables:
            module.warn('parameter "tables" is ignored when "state=absent"')
        if params:
            module.warn('parameter "parameters" is ignored when "state=absent"')
        if owner:
            module.warn('parameter "owner" is ignored when "state=absent"')
    if ((state == 'present') and cascade):
        module.warm('parameter "cascade" is ignored when "state=present"')
    conn_params = get_conn_params(module, module.params)
    db_connection = connect_to_db(module, conn_params, autocommit=True)
    cursor = db_connection.cursor(cursor_factory=DictCursor)
    if (cursor.connection.server_version < SUPPORTED_PG_VERSION):
        module.fail_json(msg='PostgreSQL server version should be 10.0 or greater')
    changed = False
    publication = PgPublication(module, cursor, name)
    if tables:
        tables = transform_tables_representation(tables)
    if (state == 'present'):
        if (not publication.exists):
            changed = publication.create(tables, params, owner, check_mode=module.check_mode)
        else:
            changed = publication.update(tables, params, owner, check_mode=module.check_mode)
    elif (state == 'absent'):
        changed = publication.drop(cascade=cascade, check_mode=module.check_mode)
    pub_fin_info = {
        
    }
    if ((state == 'present') or ((state == 'absent') and module.check_mode)):
        pub_fin_info = publication.get_info()
    elif ((state == 'absent') and (not module.check_mode)):
        publication.exists = False
    cursor.close()
    db_connection.close()
    module.exit_json(changed=changed, queries=publication.executed_queries, exists=publication.exists, **pub_fin_info)