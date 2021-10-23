

def collect(self, module=None, collected_facts=None):
    facts_dict = {
        
    }
    if (not module):
        return facts_dict
    collected_facts = (collected_facts or {
        
    })
    service_mgr_name = None
    proc_1_map = {
        'procd': 'openwrt_init',
        'runit-init': 'runit',
        'svscan': 'svc',
        'openrc-init': 'openrc',
    }
    proc_1 = get_file_content('/proc/1/comm')
    if (proc_1 is None):
        (rc, proc_1, err) = module.run_command('ps -p 1 -o comm|tail -n 1', use_unsafe_shell=True)
        if re.match(' *[0-9]+ ', proc_1):
            proc_1 = None
    if (proc_1 == 'COMMAND\n'):
        proc_1 = None
    if (proc_1 is not None):
        proc_1 = os.path.basename(proc_1)
        proc_1 = to_native(proc_1)
        proc_1 = proc_1.strip()
    if ((proc_1 is not None) and ((proc_1 == 'init') or proc_1.endswith('sh'))):
        proc_1 = None
    if (proc_1 is not None):
        service_mgr_name = proc_1_map.get(proc_1, proc_1)
    elif (collected_facts.get('distribution', None) == 'MacOSX'):
        if (LooseVersion(platform.mac_ver()[0]) >= LooseVersion('10.4')):
            service_mgr_name = 'launchd'
        else:
            service_mgr_name = 'systemstarter'
    elif (('BSD' in collected_facts.get('system', '')) or (collected_facts.get('system') in ['Bitrig', 'DragonFly'])):
        service_mgr_name = 'bsdinit'
    elif (collected_facts.get('system') == 'AIX'):
        service_mgr_name = 'src'
    elif (collected_facts.get('system') == 'SunOS'):
        service_mgr_name = 'smf'
    elif (collected_facts.get('distribution') == 'OpenWrt'):
        service_mgr_name = 'openwrt_init'
    elif (collected_facts.get('system') == 'Linux'):
        if self.is_systemd_managed(module=module):
            service_mgr_name = 'systemd'
        elif (module.get_bin_path('initctl') and os.path.exists('/etc/init/')):
            service_mgr_name = 'upstart'
        elif os.path.exists('/sbin/openrc'):
            service_mgr_name = 'openrc'
        elif os.path.exists('/etc/init.d/'):
            service_mgr_name = 'sysvinit'
    if (not service_mgr_name):
        service_mgr_name = 'service'
    facts_dict['service_mgr'] = service_mgr_name
    return facts_dict
