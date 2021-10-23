

def linodeServers(module, api, state, name, plan, distribution, datacenter, linode_id, payment_term, password, ssh_pub_key, swap, wait, wait_timeout):
    instances = []
    changed = False
    new_server = False
    servers = []
    disks = []
    configs = []
    jobs = []
    if linode_id:
        servers = api.linode_list(LinodeId=linode_id)
        if servers:
            disks = api.linode_disk_list(LinodeId=linode_id)
            configs = api.linode_config_list(LinodeId=linode_id)
    if (state in ('active', 'present', 'started')):
        if (not servers):
            for arg in ('name', 'plan', 'distribution', 'datacenter'):
                if (not eval(arg)):
                    module.fail_json(msg=('%s is required for active state' % arg))
            new_server = True
            try:
                res = api.linode_create(DatacenterID=datacenter, PlanID=plan, PaymentTerm=payment_term)
                linode_id = res['LinodeID']
                api.linode_update(LinodeId=linode_id, Label=('%s_%s' % (linode_id, name)))
                servers = api.linode_list(LinodeId=linode_id)
            except Exception as e:
                module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
        if (not disks):
            for arg in ('name', 'linode_id', 'distribution'):
                if (not eval(arg)):
                    module.fail_json(msg=('%s is required for active state' % arg))
            new_server = True
            try:
                if (not password):
                    password = randompass()
                if (not swap):
                    swap = 512
                size = (servers[0]['TOTALHD'] - swap)
                if ssh_pub_key:
                    res = api.linode_disk_createfromdistribution(LinodeId=linode_id, DistributionID=distribution, rootPass=password, rootSSHKey=ssh_pub_key, Label=('%s data disk (lid: %s)' % (name, linode_id)), Size=size)
                else:
                    res = api.linode_disk_createfromdistribution(LinodeId=linode_id, DistributionID=distribution, rootPass=password, Label=('%s data disk (lid: %s)' % (name, linode_id)), Size=size)
                jobs.append(res['JobID'])
                res = api.linode_disk_create(LinodeId=linode_id, Type='swap', Label=('%s swap disk (lid: %s)' % (name, linode_id)), Size=swap)
                jobs.append(res['JobID'])
            except Exception as e:
                module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
        if (not configs):
            for arg in ('name', 'linode_id', 'distribution'):
                if (not eval(arg)):
                    module.fail_json(msg=('%s is required for active state' % arg))
            for distrib in api.avail_distributions():
                if (distrib['DISTRIBUTIONID'] != distribution):
                    continue
                arch = '32'
                if distrib['IS64BIT']:
                    arch = '64'
                break
            for kernel in api.avail_kernels():
                if (not kernel['LABEL'].startswith(('Latest %s' % arch))):
                    continue
                kernel_id = kernel['KERNELID']
                break
            disks_id = []
            for disk in api.linode_disk_list(LinodeId=linode_id):
                if (disk['TYPE'] == 'ext3'):
                    disks_id.insert(0, str(disk['DISKID']))
                    continue
                disks_id.append(str(disk['DISKID']))
            while (len(disks_id) < 9):
                disks_id.append('')
            disks_list = ','.join(disks_id)
            new_server = True
            try:
                api.linode_config_create(LinodeId=linode_id, KernelId=kernel_id, Disklist=disks_list, Label=('%s config' % name))
                configs = api.linode_config_list(LinodeId=linode_id)
            except Exception as e:
                module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
        for server in servers:
            server = api.linode_list(LinodeId=server['LINODEID'])[0]
            if (server['STATUS'] != 1):
                res = api.linode_boot(LinodeId=linode_id)
                jobs.append(res['JobID'])
                changed = True
            wait_timeout = (time.time() + wait_timeout)
            while (wait and (wait_timeout > time.time())):
                server = api.linode_list(LinodeId=server['LINODEID'])[0]
                if (server['STATUS'] in ((- 2), 1)):
                    break
                time.sleep(5)
            if (wait and (wait_timeout <= time.time())):
                module.fail_json(msg=('Timeout waiting on %s (lid: %s)' % (server['LABEL'], server['LINODEID'])))
            server = api.linode_list(LinodeId=server['LINODEID'])[0]
            if (server['STATUS'] == (- 2)):
                module.fail_json(msg=('%s (lid: %s) failed to boot' % (server['LABEL'], server['LINODEID'])))
            instance = getInstanceDetails(api, server)
            if wait:
                instance['status'] = 'Running'
            else:
                instance['status'] = 'Starting'
            if (new_server and (not ssh_pub_key)):
                instance['password'] = password
            instances.append(instance)
    elif (state in 'stopped'):
        for arg in ('name', 'linode_id'):
            if (not eval(arg)):
                module.fail_json(msg=('%s is required for active state' % arg))
        if (not servers):
            module.fail_json(msg=('Server %s (lid: %s) not found' % (name, linode_id)))
        for server in servers:
            instance = getInstanceDetails(api, server)
            if (server['STATUS'] != 2):
                try:
                    res = api.linode_shutdown(LinodeId=linode_id)
                except Exception as e:
                    module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
                instance['status'] = 'Stopping'
                changed = True
            else:
                instance['status'] = 'Stopped'
            instances.append(instance)
    elif (state in 'restarted'):
        for arg in ('name', 'linode_id'):
            if (not eval(arg)):
                module.fail_json(msg=('%s is required for active state' % arg))
        if (not servers):
            module.fail_json(msg=('Server %s (lid: %s) not found' % (name, linode_id)))
        for server in servers:
            instance = getInstanceDetails(api, server)
            try:
                res = api.linode_reboot(LinodeId=server['LINODEID'])
            except Exception as e:
                module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
            instance['status'] = 'Restarting'
            changed = True
            instances.append(instance)
    elif (state in ('absent', 'deleted')):
        for server in servers:
            instance = getInstanceDetails(api, server)
            try:
                api.linode_delete(LinodeId=server['LINODEID'], skipChecks=True)
            except Exception as e:
                module.fail_json(msg=('%s' % e.value[0]['ERRORMESSAGE']))
            instance['status'] = 'Deleting'
            changed = True
            instances.append(instance)
    if (len(instances) == 1):
        module.exit_json(changed=changed, instance=instances[0])
    module.exit_json(changed=changed, instances=instances)
