

def main():
    '\n    This function is the main function of this module\n    '
    argument_spec = dict()
    argument_spec.update(address=dict(type='str', default='samehost', aliases=['source', 'src']), backup_file=dict(type='str'), contype=dict(type='str', default=None, choices=PG_HBA_TYPES), create=dict(type='bool', default=False), databases=dict(type='str', default='all'), dest=dict(type='path', required=True), method=dict(type='str', default='md5', choices=PG_HBA_METHODS), netmask=dict(type='str'), options=dict(type='str'), order=dict(type='str', default='sdu', choices=PG_HBA_ORDERS), state=dict(type='str', default='present', choices=['absent', 'present']), users=dict(type='str', default='all'))
    module = AnsibleModule(argument_spec=argument_spec, add_file_common_args=True, supports_check_mode=True)
    if (not HAS_IPADDRESS):
        module.fail_json(msg=missing_required_lib('psycopg2'), exception=IPADDRESS_IMP_ERR)
    contype = module.params['contype']
    create = bool((module.params['create'] or module.check_mode))
    if module.check_mode:
        backup = False
    else:
        backup = module.params['backup']
        backup_file = module.params['backup_file']
    databases = module.params['databases']
    dest = module.params['dest']
    method = module.params['method']
    netmask = module.params['netmask']
    options = module.params['options']
    order = module.params['order']
    source = module.params['address']
    state = module.params['state']
    users = module.params['users']
    ret = {
        'msgs': [],
    }
    try:
        pg_hba = PgHba(dest, order, backup=backup, create=create)
    except PgHbaError as error:
        module.fail_json(msg='Error reading file:\n{0}'.format(error))
    if contype:
        try:
            for database in databases.split(','):
                for user in users.split(','):
                    rule = PgHbaRule(contype, database, user, source, netmask, method, options)
                    if (state == 'present'):
                        ret['msgs'].append('Adding')
                        pg_hba.add_rule(rule)
                    else:
                        ret['msgs'].append('Removing')
                        pg_hba.remove_rule(rule)
        except PgHbaError as error:
            module.fail_json(msg='Error modifying rules:\n{0}'.format(error))
        file_args = module.load_file_common_arguments(module.params)
        ret['changed'] = changed = pg_hba.changed()
        if changed:
            ret['msgs'].append('Changed')
            ret['diff'] = pg_hba.diff
            if (not module.check_mode):
                ret['msgs'].append('Writing')
                try:
                    if pg_hba.write(backup_file):
                        module.set_fs_attributes_if_different(file_args, True, pg_hba.diff, expand=False)
                except PgHbaError as error:
                    module.fail_json(msg='Error writing file:\n{0}'.format(error))
                if pg_hba.last_backup:
                    ret['backup_file'] = pg_hba.last_backup
    ret['pg_hba'] = [rule for rule in pg_hba.get_rules()]
    module.exit_json(**ret)
