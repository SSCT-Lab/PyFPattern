

def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(labels=dict(type='dict', default=dict(source='ansible')), license=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present']), esxi_hostname=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    license = module.params['license']
    state = module.params['state']
    labels = []
    for k in module.params['labels']:
        kv = vim.KeyValue()
        kv.key = k
        kv.value = module.params['labels'][k]
        labels.append(kv)
    result = dict(changed=False, diff=dict())
    pyv = VcenterLicenseMgr(module)
    if (not pyv.is_vcenter()):
        module.fail_json(msg=('vcenter_license is meant for vCenter, hostname %s is not vCenter server.' % module.params.get('hostname')))
    lm = pyv.content.licenseManager
    result['licenses'] = pyv.list_keys(lm.licenses)
    if module._diff:
        result['diff']['before'] = ('\n'.join(result['licenses']) + '\n')
    if (state == 'present'):
        if (license not in result['licenses']):
            result['changed'] = True
            if module.check_mode:
                result['licenses'].append(license)
            else:
                lm.AddLicense(license, labels)
        key = pyv.find_key(lm.licenses, license)
        if (key is not None):
            lam = lm.licenseAssignmentManager
            assigned_license = None
            if (module.params['esxi_hostname'] is None):
                entityId = pyv.content.about.instanceUuid
                if (pyv.content.about.name not in key.name):
                    module.warn(('License key "%s" (%s) is not suitable for "%s"' % (license, key.name, pyv.content.about.name)))
            else:
                esxi_host = find_hostsystem_by_name(pyv.content, module.params['esxi_hostname'])
                if (esxi_host is None):
                    module.fail_json(msg=('Cannot find the specified ESXi host "%s".' % module.params['esxi_hostname']))
                entityId = esxi_host._moId
                if ('esx' not in key.editionKey):
                    module.warn(('License key "%s" edition "%s" is not suitable for ESXi server' % (license, key.editionKey)))
            try:
                assigned_license = lam.QueryAssignedLicenses(entityId=entityId)
            except Exception as e:
                module.fail_json(('Could not query vCenter "%s" assigned license info due to %s.' % (entityId, to_native(e))))
            if ((not assigned_license) or ((len(assigned_license) != 0) and (assigned_license[0].assignedLicense.licenseKey != license))):
                try:
                    lam.UpdateAssignedLicense(entity=entityId, licenseKey=license)
                except Exception:
                    module.fail_json(('Could not assign "%s" (%s) to vCenter.' % (license, key.name)))
                result['changed'] = True
            result['licenses'] = pyv.list_keys(lm.licenses)
        else:
            module.fail_json(msg=('License "%s" is not existing or can not be added' % license))
        if module._diff:
            result['diff']['after'] = ('\n'.join(result['licenses']) + '\n')
    elif ((state == 'absent') and (license in result['licenses'])):
        key = pyv.find_key(lm.licenses, license)
        if (key.used > 0):
            module.fail_json(msg=('Cannot remove key "%s", still in use %s time(s).' % (license, key.used)))
        result['changed'] = True
        if module.check_mode:
            result['licenses'].remove(license)
        else:
            lm.RemoveLicense(license)
            result['licenses'] = pyv.list_keys(lm.licenses)
        if module._diff:
            result['diff']['after'] = ('\n'.join(result['licenses']) + '\n')
    module.exit_json(**result)
