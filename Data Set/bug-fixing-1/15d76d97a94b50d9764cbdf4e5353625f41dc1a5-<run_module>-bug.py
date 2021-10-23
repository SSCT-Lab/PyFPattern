

def run_module():
    module_args = dict(name=dict(type='str', required=True), state=dict(type='str', default='present', choices=['absent', 'present']), activated=dict(type='bool'), running=dict(type='bool'), growphysical=dict(type='bool', default=False), device=dict(type='str'), logicalsize=dict(type='str'), deduplication=dict(type='str', choices=['disabled', 'enabled']), compression=dict(type='str', choices=['disabled', 'enabled']), blockmapcachesize=dict(type='str'), readcache=dict(type='str', choices=['disabled', 'enabled']), readcachesize=dict(type='str'), emulate512=dict(type='bool', default=False), slabsize=dict(type='str'), writepolicy=dict(type='str', choices=['async', 'auto', 'sync']), indexmem=dict(type='str'), indexmode=dict(type='str', choices=['dense', 'sparse']), ackthreads=dict(type='str'), biothreads=dict(type='str'), cputhreads=dict(type='str'), logicalthreads=dict(type='str'), physicalthreads=dict(type='str'))
    result = dict(changed=False)
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=False)
    if (not HAS_YAML):
        module.fail_json(msg=missing_required_lib('PyYAML'), exception=YAML_IMP_ERR)
    vdocmd = module.get_bin_path('vdo', required=True)
    if (not vdocmd):
        module.fail_json(msg='VDO is not installed.', **result)
    vdolist = inventory_vdos(module, vdocmd)
    runningvdolist = list_running_vdos(module, vdocmd)
    desiredvdo = module.params['name']
    state = module.params['state']
    if ((desiredvdo not in vdolist) and (state == 'present')):
        device = module.params['device']
        if (device is None):
            module.fail_json(msg="Creating a VDO volume requires specifying a 'device' in the playbook.")
        options = module.params
        vdocmdoptions = add_vdooptions(options)
        (rc, out, err) = module.run_command(('%s create --name=%s --device=%s %s' % (vdocmd, desiredvdo, device, vdocmdoptions)))
        if (rc == 0):
            result['changed'] = True
        else:
            module.fail_json(msg=('Creating VDO %s failed.' % desiredvdo), rc=rc, err=err)
        if (module.params['compression'] == 'disabled'):
            (rc, out, err) = module.run_command(('%s disableCompression --name=%s' % (vdocmd, desiredvdo)))
        if ((module.params['deduplication'] is not None) and (module.params['deduplication'] == 'disabled')):
            (rc, out, err) = module.run_command(('%s disableDeduplication --name=%s' % (vdocmd, desiredvdo)))
        if (module.params['activated'] == 'no'):
            deactivate_vdo(module, desiredvdo, vdocmd)
        if (module.params['running'] == 'no'):
            stop_vdo(module, desiredvdo, vdocmd)
        vdolist = inventory_vdos(module, vdocmd)
        module.log(('created VDO volume %s' % desiredvdo))
        module.exit_json(**result)
    if ((desiredvdo in vdolist) and (state == 'present')):
        (rc, vdostatusoutput, err) = module.run_command(('%s status' % vdocmd))
        vdostatusyaml = yaml.load(vdostatusoutput)
        processedvdos = {
            
        }
        vdoyamls = vdostatusyaml['VDOs']
        if (vdoyamls is not None):
            processedvdos = vdoyamls
        statusparamkeys = ['Acknowledgement threads', 'Bio submission threads', 'Block map cache size', 'CPU-work threads', 'Logical threads', 'Physical threads', 'Read cache', 'Read cache size', 'Configured write policy', 'Compression', 'Deduplication']
        vdokeytrans = {
            'Logical size': 'logicalsize',
            'Compression': 'compression',
            'Deduplication': 'deduplication',
            'Block map cache size': 'blockmapcachesize',
            'Read cache': 'readcache',
            'Read cache size': 'readcachesize',
            'Configured write policy': 'writepolicy',
            'Acknowledgement threads': 'ackthreads',
            'Bio submission threads': 'biothreads',
            'CPU-work threads': 'cputhreads',
            'Logical threads': 'logicalthreads',
            'Physical threads': 'physicalthreads',
        }
        currentvdoparams = {
            
        }
        modtrans = {
            
        }
        for statfield in statusparamkeys:
            currentvdoparams[statfield] = processedvdos[desiredvdo][statfield]
            modtrans[statfield] = vdokeytrans[statfield]
        currentparams = {
            
        }
        for paramkey in currentvdoparams.keys():
            currentparams[modtrans[paramkey]] = currentvdoparams[paramkey]
        diffparams = {
            
        }
        for key in currentparams.keys():
            if (module.params[key] is not None):
                if (str(currentparams[key]) != module.params[key]):
                    diffparams[key] = module.params[key]
        if diffparams:
            vdocmdoptions = add_vdooptions(diffparams)
            if vdocmdoptions:
                (rc, out, err) = module.run_command(('%s modify --name=%s %s' % (vdocmd, desiredvdo, vdocmdoptions)))
                if (rc == 0):
                    result['changed'] = True
                else:
                    module.fail_json(msg=('Modifying VDO %s failed.' % desiredvdo), rc=rc, err=err)
            if ('deduplication' in diffparams.keys()):
                dedupemod = diffparams['deduplication']
                if (dedupemod == 'disabled'):
                    (rc, out, err) = module.run_command(('%s disableDeduplication --name=%s' % (vdocmd, desiredvdo)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing deduplication on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
                if (dedupemod == 'enabled'):
                    (rc, out, err) = module.run_command(('%s enableDeduplication --name=%s' % (vdocmd, desiredvdo)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing deduplication on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
            if ('compression' in diffparams.keys()):
                compressmod = diffparams['compression']
                if (compressmod == 'disabled'):
                    (rc, out, err) = module.run_command(('%s disableCompression --name=%s' % (vdocmd, desiredvdo)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing compression on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
                if (compressmod == 'enabled'):
                    (rc, out, err) = module.run_command(('%s enableCompression --name=%s' % (vdocmd, desiredvdo)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing compression on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
            if ('writepolicy' in diffparams.keys()):
                writepolmod = diffparams['writepolicy']
                if (writepolmod == 'auto'):
                    (rc, out, err) = module.run_command(('%s changeWritePolicy --name=%s --writePolicy=%s' % (vdocmd, desiredvdo, writepolmod)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing write policy on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
                if (writepolmod == 'sync'):
                    (rc, out, err) = module.run_command(('%s changeWritePolicy --name=%s --writePolicy=%s' % (vdocmd, desiredvdo, writepolmod)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing write policy on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
                if (writepolmod == 'async'):
                    (rc, out, err) = module.run_command(('%s changeWritePolicy --name=%s --writePolicy=%s' % (vdocmd, desiredvdo, writepolmod)))
                    if (rc == 0):
                        result['changed'] = True
                    else:
                        module.fail_json(msg=('Changing write policy on VDO volume %s failed.' % desiredvdo), rc=rc, err=err)
        sizeparamkeys = ['Logical size']
        currentsizeparams = {
            
        }
        sizetrans = {
            
        }
        for statfield in sizeparamkeys:
            currentsizeparams[statfield] = processedvdos[desiredvdo][statfield]
            sizetrans[statfield] = vdokeytrans[statfield]
        sizeparams = {
            
        }
        for paramkey in currentsizeparams.keys():
            sizeparams[sizetrans[paramkey]] = currentsizeparams[paramkey]
        diffsizeparams = {
            
        }
        for key in sizeparams.keys():
            if (module.params[key] is not None):
                if (str(sizeparams[key]) != module.params[key]):
                    diffsizeparams[key] = module.params[key]
        if module.params['growphysical']:
            physdevice = module.params['device']
            (rc, devsectors, err) = module.run_command(('blockdev --getsz %s' % physdevice))
            devblocks = (int(devsectors) / 8)
            dmvdoname = ('/dev/mapper/' + desiredvdo)
            currentvdostats = processedvdos[desiredvdo]['VDO statistics'][dmvdoname]
            currentphysblocks = currentvdostats['physical blocks']
            growthresh = (devblocks + 16777216)
            if (currentphysblocks > growthresh):
                result['changed'] = True
                (rc, out, err) = module.run_command(('%s growPhysical --name=%s' % (vdocmd, desiredvdo)))
        if ('logicalsize' in diffsizeparams.keys()):
            result['changed'] = True
            vdocmdoptions = ('--vdoLogicalSize=' + diffsizeparams['logicalsize'])
            (rc, out, err) = module.run_command(('%s growLogical --name=%s %s' % (vdocmd, desiredvdo, vdocmdoptions)))
        vdoactivatestatus = processedvdos[desiredvdo]['Activate']
        if ((module.params['activated'] == 'no') and (vdoactivatestatus == 'enabled')):
            deactivate_vdo(module, desiredvdo, vdocmd)
            if (not result['changed']):
                result['changed'] = True
        if ((module.params['activated'] == 'yes') and (vdoactivatestatus == 'disabled')):
            activate_vdo(module, desiredvdo, vdocmd)
            if (not result['changed']):
                result['changed'] = True
        if ((module.params['running'] == 'no') and (desiredvdo in runningvdolist)):
            stop_vdo(module, desiredvdo, vdocmd)
            if (not result['changed']):
                result['changed'] = True
        if (((vdoactivatestatus == 'enabled') or (module.params['activated'] == 'yes')) and (module.params['running'] == 'yes') and (desiredvdo not in runningvdolist)):
            start_vdo(module, desiredvdo, vdocmd)
            if (not result['changed']):
                result['changed'] = True
        vdolist = inventory_vdos(module, vdocmd)
        if diffparams:
            module.log(('modified parameters of VDO volume %s' % desiredvdo))
        module.exit_json(**result)
    if ((desiredvdo in vdolist) and (state == 'absent')):
        (rc, out, err) = module.run_command(('%s remove --name=%s' % (vdocmd, desiredvdo)))
        if (rc == 0):
            result['changed'] = True
        else:
            module.fail_json(msg=('Removing VDO %s failed.' % desiredvdo), rc=rc, err=err)
        vdolist = inventory_vdos(module, vdocmd)
        module.log(('removed VDO volume %s' % desiredvdo))
        module.exit_json(**result)
    vdolist = inventory_vdos(module, vdocmd)
    module.log(('received request to remove non-existent VDO volume %s' % desiredvdo))
    module.exit_json(**result)
