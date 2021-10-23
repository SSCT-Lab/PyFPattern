def main():
    module = AnsibleModule(argument_spec=dict(vg=dict(required=True), lv=dict(required=True), size=dict(type='str'), opts=dict(type='str'), state=dict(choices=['absent', 'present'], default='present'), force=dict(type='bool', default='no'), shrink=dict(type='bool', default='yes'), active=dict(type='bool', default='yes'), snapshot=dict(type='str', default=None), pvs=dict(type='str')), supports_check_mode=True)
    version_found = get_lvm_version(module)
    if (version_found is None):
        module.fail_json(msg='Failed to get LVM version number')
    version_yesopt = mkversion(2, 2, 99)
    if (version_found >= version_yesopt):
        yesopt = '--yes'
    else:
        yesopt = ''
    vg = module.params['vg']
    lv = module.params['lv']
    size = module.params['size']
    opts = module.params['opts']
    state = module.params['state']
    force = module.boolean(module.params['force'])
    shrink = module.boolean(module.params['shrink'])
    active = module.boolean(module.params['active'])
    size_opt = 'L'
    size_unit = 'm'
    snapshot = module.params['snapshot']
    pvs = module.params['pvs']
    if (pvs is None):
        pvs = ''
    else:
        pvs = pvs.replace(',', ' ')
    if (opts is None):
        opts = ''
    if module.check_mode:
        test_opt = ' --test'
    else:
        test_opt = ''
    if size:
        if ('%' in size):
            size_parts = size.split('%', 1)
            size_percent = int(size_parts[0])
            if (size_percent > 100):
                module.fail_json(msg='Size percentage cannot be larger than 100%')
            size_whole = size_parts[1]
            if (size_whole == 'ORIGIN'):
                module.fail_json(msg='Snapshot Volumes are not supported')
            elif (size_whole not in ['VG', 'PVS', 'FREE']):
                module.fail_json(msg='Specify extents as a percentage of VG|PVS|FREE')
            size_opt = 'l'
            size_unit = ''
        if (not ('%' in size)):
            if (size[(- 1)].lower() in 'bskmgtpe'):
                size_unit = size[(- 1)].lower()
                size = size[0:(- 1)]
            try:
                float(size)
                if (not size[0].isdigit()):
                    raise ValueError()
            except ValueError:
                module.fail_json(msg=("Bad size specification of '%s'" % size))
    if (size_opt == 'l'):
        unit = 'm'
    else:
        unit = size_unit
    vgs_cmd = module.get_bin_path('vgs', required=True)
    (rc, current_vgs, err) = module.run_command(("%s --noheadings -o vg_name,size,free,vg_extent_size --units %s --separator ';' %s" % (vgs_cmd, unit, vg)))
    if (rc != 0):
        if (state == 'absent'):
            module.exit_json(changed=False, stdout=('Volume group %s does not exist.' % vg))
        else:
            module.fail_json(msg=('Volume group %s does not exist.' % vg), rc=rc, err=err)
    vgs = parse_vgs(current_vgs)
    this_vg = vgs[0]
    lvs_cmd = module.get_bin_path('lvs', required=True)
    (rc, current_lvs, err) = module.run_command(("%s -a --noheadings --nosuffix -o lv_name,size,lv_attr --units %s --separator ';' %s" % (lvs_cmd, unit, vg)))
    if (rc != 0):
        if (state == 'absent'):
            module.exit_json(changed=False, stdout=('Volume group %s does not exist.' % vg))
        else:
            module.fail_json(msg=('Volume group %s does not exist.' % vg), rc=rc, err=err)
    changed = False
    lvs = parse_lvs(current_lvs)
    if (snapshot is None):
        check_lv = lv
    else:
        check_lv = snapshot
    for test_lv in lvs:
        if (test_lv['name'] == check_lv):
            this_lv = test_lv
            break
    else:
        this_lv = None
    if ((state == 'present') and (not size)):
        if (this_lv is None):
            module.fail_json(msg='No size given.')
    msg = ''
    if (this_lv is None):
        if (state == 'present'):
            lvcreate_cmd = module.get_bin_path('lvcreate', required=True)
            if (snapshot is not None):
                cmd = ('%s %s %s -%s %s%s -s -n %s %s %s/%s' % (lvcreate_cmd, test_opt, yesopt, size_opt, size, size_unit, snapshot, opts, vg, lv))
            else:
                cmd = ('%s %s %s -n %s -%s %s%s %s %s %s' % (lvcreate_cmd, test_opt, yesopt, lv, size_opt, size, size_unit, opts, vg, pvs))
            (rc, _, err) = module.run_command(cmd)
            if (rc == 0):
                changed = True
            else:
                module.fail_json(msg=("Creating logical volume '%s' failed" % lv), rc=rc, err=err)
    elif (state == 'absent'):
        if (not force):
            module.fail_json(msg=('Sorry, no removal of logical volume %s without force=yes.' % this_lv['name']))
        lvremove_cmd = module.get_bin_path('lvremove', required=True)
        (rc, _, err) = module.run_command(('%s %s --force %s/%s' % (lvremove_cmd, test_opt, vg, this_lv['name'])))
        if (rc == 0):
            module.exit_json(changed=True)
        else:
            module.fail_json(msg=('Failed to remove logical volume %s' % lv), rc=rc, err=err)
    elif (not size):
        pass
    elif (size_opt == 'l'):
        tool = None
        size_free = this_vg['free']
        if ((size_whole == 'VG') or (size_whole == 'PVS')):
            size_requested = ((size_percent * this_vg['size']) / 100)
        else:
            size_requested = ((size_percent * this_vg['free']) / 100)
        if ('+' in size):
            size_requested += this_lv['size']
        if (this_lv['size'] < size_requested):
            if ((size_free > 0) and (('+' not in size) or (size_free >= (size_requested - this_lv['size'])))):
                tool = module.get_bin_path('lvextend', required=True)
            else:
                module.fail_json(msg=('Logical Volume %s could not be extended. Not enough free space left (%s%s required / %s%s available)' % (this_lv['name'], (size_requested - this_lv['size']), unit, size_free, unit)))
        elif (shrink and (this_lv['size'] > (size_requested + this_vg['ext_size']))):
            if (size_requested == 0):
                module.fail_json(msg=('Sorry, no shrinking of %s to 0 permitted.' % this_lv['name']))
            elif (not force):
                module.fail_json(msg=('Sorry, no shrinking of %s without force=yes' % this_lv['name']))
            else:
                tool = module.get_bin_path('lvreduce', required=True)
                tool = ('%s %s' % (tool, '--force'))
        if tool:
            cmd = ('%s %s -%s %s%s %s/%s %s' % (tool, test_opt, size_opt, size, size_unit, vg, this_lv['name'], pvs))
            (rc, out, err) = module.run_command(cmd)
            if ('Reached maximum COW size' in out):
                module.fail_json(msg=('Unable to resize %s to %s%s' % (lv, size, size_unit)), rc=rc, err=err, out=out)
            elif (rc == 0):
                changed = True
                msg = ('Volume %s resized to %s%s' % (this_lv['name'], size_requested, unit))
            elif ('matches existing size' in err):
                module.exit_json(changed=False, vg=vg, lv=this_lv['name'], size=this_lv['size'])
            elif ('not larger than existing size' in err):
                module.exit_json(changed=False, vg=vg, lv=this_lv['name'], size=this_lv['size'], msg='Original size is larger than requested size', err=err)
            else:
                module.fail_json(msg=('Unable to resize %s to %s%s' % (lv, size, size_unit)), rc=rc, err=err)
    else:
        tool = None
        if (int(size) > this_lv['size']):
            tool = module.get_bin_path('lvextend', required=True)
        elif (shrink and (int(size) < this_lv['size'])):
            if (int(size) == 0):
                module.fail_json(msg=('Sorry, no shrinking of %s to 0 permitted.' % this_lv['name']))
            if (not force):
                module.fail_json(msg=('Sorry, no shrinking of %s without force=yes.' % this_lv['name']))
            else:
                tool = module.get_bin_path('lvreduce', required=True)
                tool = ('%s %s' % (tool, '--force'))
        if tool:
            cmd = ('%s %s -%s %s%s %s/%s %s' % (tool, test_opt, size_opt, size, size_unit, vg, this_lv['name'], pvs))
            (rc, out, err) = module.run_command(cmd)
            if ('Reached maximum COW size' in out):
                module.fail_json(msg=('Unable to resize %s to %s%s' % (lv, size, size_unit)), rc=rc, err=err, out=out)
            elif (rc == 0):
                changed = True
            elif ('matches existing size' in err):
                module.exit_json(changed=False, vg=vg, lv=this_lv['name'], size=this_lv['size'])
            elif ('not larger than existing size' in err):
                module.exit_json(changed=False, vg=vg, lv=this_lv['name'], size=this_lv['size'], msg='Original size is larger than requested size', err=err)
            else:
                module.fail_json(msg=('Unable to resize %s to %s%s' % (lv, size, size_unit)), rc=rc, err=err)
    if (this_lv is not None):
        if active:
            lvchange_cmd = module.get_bin_path('lvchange', required=True)
            (rc, _, err) = module.run_command(('%s -ay %s/%s' % (lvchange_cmd, vg, this_lv['name'])))
            if (rc == 0):
                module.exit_json(changed=((not this_lv['active']) or changed), vg=vg, lv=this_lv['name'], size=this_lv['size'])
            else:
                module.fail_json(msg=('Failed to activate logical volume %s' % lv), rc=rc, err=err)
        else:
            lvchange_cmd = module.get_bin_path('lvchange', required=True)
            (rc, _, err) = module.run_command(('%s -an %s/%s' % (lvchange_cmd, vg, this_lv['name'])))
            if (rc == 0):
                module.exit_json(changed=(this_lv['active'] or changed), vg=vg, lv=this_lv['name'], size=this_lv['size'])
            else:
                module.fail_json(msg=('Failed to deactivate logical volume %s' % lv), rc=rc, err=err)
    module.exit_json(changed=changed, msg=msg)