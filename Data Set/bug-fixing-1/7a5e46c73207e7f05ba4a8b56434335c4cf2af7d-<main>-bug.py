

def main():
    module = AnsibleModule(argument_spec=dict(vg=dict(required=True, type='str'), lv=dict(required=True, type='str'), lv_type=dict(default='jfs2', type='str'), size=dict(type='str'), opts=dict(default='', type='str'), copies=dict(default='1', type='str'), state=dict(choices=['absent', 'present'], default='present'), policy=dict(choices=['maximum', 'minimum'], default='maximum'), pvs=dict(type='list', default=list())), supports_check_mode=True)
    vg = module.params['vg']
    lv = module.params['lv']
    lv_type = module.params['lv_type']
    size = module.params['size']
    opts = module.params['opts']
    copies = module.params['copies']
    policy = module.params['policy']
    state = module.params['state']
    pvs = module.params['pvs']
    pv_list = ' '.join(pvs)
    if (policy == 'maximum'):
        lv_policy = 'x'
    else:
        lv_policy = 'm'
    if module.check_mode:
        test_opt = 'echo '
    else:
        test_opt = ''
    lsvg_cmd = module.get_bin_path('lsvg', required=True)
    lslv_cmd = module.get_bin_path('lslv', required=True)
    (rc, vg_info, err) = module.run_command(('%s %s' % (lsvg_cmd, vg)))
    if (rc != 0):
        if (state == 'absent'):
            module.exit_json(changed=False, msg=('Volume group %s does not exist.' % vg))
        else:
            module.fail_json(msg=('Volume group %s does not exist.' % vg), rc=rc, out=vg_info, err=err)
    this_vg = parse_vg(vg_info)
    if (size is not None):
        lv_size = round_ppsize(convert_size(module, size), base=this_vg['pp_size'])
    (rc, lv_info, err) = module.run_command(('%s %s' % (lslv_cmd, lv)))
    if (rc != 0):
        if (state == 'absent'):
            module.exit_json(changed=False, msg=('Logical Volume %s does not exist.' % lv))
    changed = False
    this_lv = parse_lv(lv_info)
    if ((state == 'present') and (not size)):
        if (this_lv is None):
            module.fail_json(msg='No size given.')
    if (this_lv is None):
        if (state == 'present'):
            if (lv_size > this_vg['free']):
                module.fail_json(msg=('Not enough free space in volume group %s: %s MB free.' % (this_vg['name'], this_vg['free'])))
            mklv_cmd = module.get_bin_path('mklv', required=True)
            cmd = ('%s %s -t %s -y %s -c %s  -e %s %s %s %sM %s' % (test_opt, mklv_cmd, lv_type, lv, copies, lv_policy, opts, vg, lv_size, pv_list))
            (rc, out, err) = module.run_command(cmd)
            if (rc == 0):
                module.exit_json(changed=True, msg=('Logical volume %s created.' % lv))
            else:
                module.fail_json(msg=('Creating logical volume %s failed.' % lv), rc=rc, out=out, err=err)
    elif (state == 'absent'):
        rmlv_cmd = module.get_bin_path('rmlv', required=True)
        (rc, out, err) = module.run_command(('%s %s -f %s' % (test_opt, rmlv_cmd, this_lv['name'])))
        if (rc == 0):
            module.exit_json(changed=True, msg=('Logical volume %s deleted.' % lv))
        else:
            module.fail_json(msg=('Failed to remove logical volume %s.' % lv), rc=rc, out=out, err=err)
    else:
        if (this_lv['policy'] != policy):
            chlv_cmd = module.get_bin_path('chlv', required=True)
            (rc, out, err) = module.run_command(('%s %s -e %s %s' % (test_opt, chlv_cmd, lv_policy, this_lv['name'])))
            if (rc == 0):
                module.exit_json(changed=True, msg=('Logical volume %s policy changed: %s.' % (lv, policy)))
            else:
                module.fail_json(msg=('Failed to change logical volume %s policy.' % lv), rc=rc, out=out, err=err)
        if (vg != this_lv['vg']):
            module.fail_json(msg=('Logical volume %s already exist in volume group %s' % (lv, this_lv['vg'])))
        if (not size):
            module.exit_json(changed=False, msg=('Logical volume %s already exist.' % lv))
        if (int(lv_size) > this_lv['size']):
            extendlv_cmd = module.get_bin_path('extendlv', required=True)
            cmd = ('%s %s %s %sM' % (test_opt, extendlv_cmd, lv, (lv_size - this_lv['size'])))
            (rc, out, err) = module.run_command(cmd)
            if (rc == 0):
                module.exit_json(changed=True, msg=('Logical volume %s size extended to %sMB.' % (lv, lv_size)))
            else:
                module.fail_json(msg=('Unable to resize %s to %sMB.' % (lv, lv_size)), rc=rc, out=out, err=err)
        elif (lv_size < this_lv['size']):
            module.fail_json(msg=('No shrinking of Logical Volume %s permitted. Current size: %s MB' % (lv, this_lv['size'])))
        else:
            module.exit_json(changed=False, msg=('Logical volume %s size is already %sMB.' % (lv, lv_size)))
