def main():
    module = AnsibleModule(argument_spec=dict(vg=dict(type='str', required=True), pvs=dict(type='list'), pesize=dict(type='int', default=4), pv_options=dict(type='str', default=''), vg_options=dict(type='str', default=''), state=dict(type='str', default='present', choices=['absent', 'present']), force=dict(type='bool', default=False)), supports_check_mode=True)
    vg = module.params['vg']
    state = module.params['state']
    force = module.boolean(module.params['force'])
    pesize = module.params['pesize']
    pvoptions = module.params['pv_options'].split()
    vgoptions = module.params['vg_options'].split()
    dev_list = []
    if module.params['pvs']:
        dev_list = module.params['pvs']
    elif (state == 'present'):
        module.fail_json(msg='No physical volumes given.')
    for (idx, dev) in enumerate(dev_list):
        dev_list[idx] = os.path.realpath(dev)
    if (state == 'present'):
        for test_dev in dev_list:
            if (not os.path.exists(test_dev)):
                module.fail_json(msg=('Device %s not found.' % test_dev))
        pvs_cmd = module.get_bin_path('pvs', True)
        if dev_list:
            pvs_filter = ' || '.join(['pv_name = {0}'.format(x) for x in dev_list])
            pvs_filter = ("--select '%s'" % pvs_filter)
        else:
            pvs_filter = ''
        (rc, current_pvs, err) = module.run_command(("%s --noheadings -o pv_name,vg_name --separator ';' %s" % (pvs_cmd, pvs_filter)))
        if (rc != 0):
            module.fail_json(msg='Failed executing pvs command.', rc=rc, err=err)
        pvs = parse_pvs(module, current_pvs)
        used_pvs = [pv for pv in pvs if ((pv['name'] in dev_list) and pv['vg_name'] and (pv['vg_name'] != vg))]
        if used_pvs:
            module.fail_json(msg=('Device %s is already in %s volume group.' % (used_pvs[0]['name'], used_pvs[0]['vg_name'])))
    vgs_cmd = module.get_bin_path('vgs', True)
    (rc, current_vgs, err) = module.run_command(("%s --noheadings -o vg_name,pv_count,lv_count --separator ';'" % vgs_cmd))
    if (rc != 0):
        module.fail_json(msg='Failed executing vgs command.', rc=rc, err=err)
    changed = False
    vgs = parse_vgs(current_vgs)
    for test_vg in vgs:
        if (test_vg['name'] == vg):
            this_vg = test_vg
            break
    else:
        this_vg = None
    if (this_vg is None):
        if (state == 'present'):
            if module.check_mode:
                changed = True
            else:
                pvcreate_cmd = module.get_bin_path('pvcreate', True)
                for current_dev in dev_list:
                    (rc, _, err) = module.run_command((([pvcreate_cmd] + pvoptions) + ['-f', str(current_dev)]))
                    if (rc == 0):
                        changed = True
                    else:
                        module.fail_json(msg=("Creating physical volume '%s' failed" % current_dev), rc=rc, err=err)
                vgcreate_cmd = module.get_bin_path('vgcreate')
                (rc, _, err) = module.run_command(((([vgcreate_cmd] + vgoptions) + ['-s', str(pesize), vg]) + dev_list))
                if (rc == 0):
                    changed = True
                else:
                    module.fail_json(msg=("Creating volume group '%s' failed" % vg), rc=rc, err=err)
    else:
        if (state == 'absent'):
            if module.check_mode:
                module.exit_json(changed=True)
            elif ((this_vg['lv_count'] == 0) or force):
                vgremove_cmd = module.get_bin_path('vgremove', True)
                (rc, _, err) = module.run_command(('%s --force %s' % (vgremove_cmd, vg)))
                if (rc == 0):
                    module.exit_json(changed=True)
                else:
                    module.fail_json(msg=('Failed to remove volume group %s' % vg), rc=rc, err=err)
            else:
                module.fail_json(msg=('Refuse to remove non-empty volume group %s without force=yes' % vg))
        current_devs = [os.path.realpath(pv['name']) for pv in pvs if (pv['vg_name'] == vg)]
        devs_to_remove = list((set(current_devs) - set(dev_list)))
        devs_to_add = list((set(dev_list) - set(current_devs)))
        if (devs_to_add or devs_to_remove):
            if module.check_mode:
                changed = True
            else:
                if devs_to_add:
                    devs_to_add_string = ' '.join(devs_to_add)
                    pvcreate_cmd = module.get_bin_path('pvcreate', True)
                    for current_dev in devs_to_add:
                        (rc, _, err) = module.run_command((([pvcreate_cmd] + pvoptions) + ['-f', str(current_dev)]))
                        if (rc == 0):
                            changed = True
                        else:
                            module.fail_json(msg=("Creating physical volume '%s' failed" % current_dev), rc=rc, err=err)
                    vgextend_cmd = module.get_bin_path('vgextend', True)
                    (rc, _, err) = module.run_command(('%s %s %s' % (vgextend_cmd, vg, devs_to_add_string)))
                    if (rc == 0):
                        changed = True
                    else:
                        module.fail_json(msg=('Unable to extend %s by %s.' % (vg, devs_to_add_string)), rc=rc, err=err)
                if devs_to_remove:
                    devs_to_remove_string = ' '.join(devs_to_remove)
                    vgreduce_cmd = module.get_bin_path('vgreduce', True)
                    (rc, _, err) = module.run_command(('%s --force %s %s' % (vgreduce_cmd, vg, devs_to_remove_string)))
                    if (rc == 0):
                        changed = True
                    else:
                        module.fail_json(msg=('Unable to reduce %s by %s.' % (vg, devs_to_remove_string)), rc=rc, err=err)
    module.exit_json(changed=changed)