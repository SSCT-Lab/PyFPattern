

def main():
    expiry = date.strftime((date.today() + timedelta(days=365)), '%Y-%m-%d')
    module = AnsibleModule(argument_spec=dict(birthday=dict(default=None, type='str'), city=dict(default=None, type='str'), country=dict(default=None, type='str'), department_number=dict(default=None, type='str', aliases=['departmentNumber']), description=dict(default=None, type='str'), display_name=dict(default=None, type='str', aliases=['displayName']), email=dict(default=[''], type='list'), employee_number=dict(default=None, type='str', aliases=['employeeNumber']), employee_type=dict(default=None, type='str', aliases=['employeeType']), firstname=dict(default=None, type='str'), gecos=dict(default=None, type='str'), groups=dict(default=[], type='list'), home_share=dict(default=None, type='str', aliases=['homeShare']), home_share_path=dict(default=None, type='str', aliases=['homeSharePath']), home_telephone_number=dict(default=[], type='list', aliases=['homeTelephoneNumber']), homedrive=dict(default=None, type='str'), lastname=dict(default=None, type='str'), mail_alternative_address=dict(default=[], type='list', aliases=['mailAlternativeAddress']), mail_home_server=dict(default=None, type='str', aliases=['mailHomeServer']), mail_primary_address=dict(default=None, type='str', aliases=['mailPrimaryAddress']), mobile_telephone_number=dict(default=[], type='list', aliases=['mobileTelephoneNumber']), organisation=dict(default=None, type='str', aliases=['organization']), overridePWHistory=dict(default=False, type='bool', aliases=['override_pw_history']), overridePWLength=dict(default=False, type='bool', aliases=['override_pw_length']), pager_telephonenumber=dict(default=[], type='list', aliases=['pagerTelephonenumber']), password=dict(default=None, type='str', no_log=True), phone=dict(default=[], type='list'), postcode=dict(default=None, type='str'), primary_group=dict(default=None, type='str', aliases=['primaryGroup']), profilepath=dict(default=None, type='str'), pwd_change_next_login=dict(default=None, type='str', choices=['0', '1'], aliases=['pwdChangeNextLogin']), room_number=dict(default=None, type='str', aliases=['roomNumber']), samba_privileges=dict(default=[], type='list', aliases=['sambaPrivileges']), samba_user_workstations=dict(default=[], type='list', aliases=['sambaUserWorkstations']), sambahome=dict(default=None, type='str'), scriptpath=dict(default=None, type='str'), secretary=dict(default=[], type='list'), serviceprovider=dict(default=[''], type='list'), shell=dict(default='/bin/bash', type='str'), street=dict(default=None, type='str'), title=dict(default=None, type='str'), unixhome=dict(default=None, type='str'), userexpiry=dict(default=expiry, type='str'), username=dict(required=True, aliases=['name'], type='str'), position=dict(default='', type='str'), update_password=dict(default='always', choices=['always', 'on_create'], type='str'), ou=dict(default='', type='str'), subpath=dict(default='cn=users', type='str'), state=dict(default='present', choices=['present', 'absent'], type='str')), supports_check_mode=True, required_if=[('state', 'present', ['firstname', 'lastname', 'password'])])
    username = module.params['username']
    position = module.params['position']
    ou = module.params['ou']
    subpath = module.params['subpath']
    state = module.params['state']
    changed = False
    users = list(ldap_search('(&(objectClass=posixAccount)(uid={}))'.format(username), attr=['uid']))
    if (position != ''):
        container = position
    else:
        if (ou != ''):
            ou = 'ou={},'.format(ou)
        if (subpath != ''):
            subpath = '{},'.format(subpath)
        container = '{}{}{}'.format(subpath, ou, base_dn())
    user_dn = 'uid={},{}'.format(username, container)
    exists = bool(len(users))
    if (state == 'present'):
        try:
            if (not exists):
                obj = umc_module_for_add('users/user', container)
            else:
                obj = umc_module_for_edit('users/user', user_dn)
            if (module.params['displayName'] is None):
                module.params['displayName'] = '{} {}'.format(module.params['firstname'], module.params['lastname'])
            if (module.params['unixhome'] is None):
                module.params['unixhome'] = '/home/{}'.format(module.params['username'])
            for k in obj.keys():
                if ((k != 'password') and (k != 'groups') and (k != 'overridePWHistory') and (k in module.params) and (module.params[k] is not None)):
                    obj[k] = module.params[k]
            obj['e-mail'] = module.params['email']
            password = module.params['password']
            if (obj['password'] is None):
                obj['password'] = password
            if (module.params['update_password'] == 'always'):
                old_password = obj['password'].split('}', 2)[1]
                if (crypt.crypt(password, old_password) != old_password):
                    obj['overridePWHistory'] = module.params['overridePWHistory']
                    obj['overridePWLength'] = module.params['overridePWLength']
                    obj['password'] = password
            diff = obj.diff()
            if exists:
                for k in obj.keys():
                    if obj.hasChanged(k):
                        changed = True
            else:
                changed = True
            if (not module.check_mode):
                if (not exists):
                    obj.create()
                elif changed:
                    obj.modify()
        except:
            module.fail_json(msg='Creating/editing user {} in {} failed'.format(username, container))
        try:
            groups = module.params['groups']
            if groups:
                filter = '(&(objectClass=posixGroup)(|(cn={})))'.format(')(cn='.join(groups))
                group_dns = list(ldap_search(filter, attr=['dn']))
                for dn in group_dns:
                    grp = umc_module_for_edit('groups/group', dn[0])
                    if (user_dn not in grp['users']):
                        grp['users'].append(user_dn)
                        if (not module.check_mode):
                            grp.modify()
                        changed = True
        except:
            module.fail_json(msg='Adding groups to user {} failed'.format(username))
    if ((state == 'absent') and exists):
        try:
            obj = umc_module_for_edit('users/user', user_dn)
            if (not module.check_mode):
                obj.remove()
            changed = True
        except:
            module.fail_json(msg='Removing user {} failed'.format(username))
    module.exit_json(changed=changed, username=username, diff=diff, container=container)
