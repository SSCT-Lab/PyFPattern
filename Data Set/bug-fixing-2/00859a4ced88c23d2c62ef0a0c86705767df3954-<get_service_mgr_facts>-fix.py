

def get_service_mgr_facts(self):
    proc_1_map = {
        'procd': 'openwrt_init',
    }
    proc_1 = get_file_content('/proc/1/comm')
    if (proc_1 is None):
        (rc, proc_1, err) = self.module.run_command('ps -p 1 -o comm|tail -n 1', use_unsafe_shell=True)
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
        self.facts['service_mgr'] = proc_1_map.get(proc_1, proc_1)
    elif (self.facts['distribution'] == 'MacOSX'):
        if (LooseVersion(platform.mac_ver()[0]) >= LooseVersion('10.4')):
            self.facts['service_mgr'] = 'launchd'
        else:
            self.facts['service_mgr'] = 'systemstarter'
    elif (('BSD' in self.facts['system']) or (self.facts['system'] in ['Bitrig', 'DragonFly'])):
        self.facts['service_mgr'] = 'bsdinit'
    elif (self.facts['system'] == 'AIX'):
        self.facts['service_mgr'] = 'src'
    elif (self.facts['system'] == 'SunOS'):
        self.facts['service_mgr'] = 'svcs'
    elif (self.facts['distribution'] == 'OpenWrt'):
        self.facts['service_mgr'] = 'openwrt_init'
    elif (self.facts['system'] == 'Linux'):
        if self.is_systemd_managed():
            self.facts['service_mgr'] = 'systemd'
        elif (self.module.get_bin_path('initctl') and os.path.exists('/etc/init/')):
            self.facts['service_mgr'] = 'upstart'
        elif (os.path.realpath('/sbin/rc') == '/sbin/openrc'):
            self.facts['service_mgr'] = 'openrc'
        elif os.path.exists('/etc/init.d/'):
            self.facts['service_mgr'] = 'sysvinit'
    if (not self.facts.get('service_mgr', False)):
        self.facts['service_mgr'] = 'service'
