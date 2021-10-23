

def get_device_facts(self):
    device_facts = {
        
    }
    device_facts['devices'] = {
        
    }
    lspci = self.module.get_bin_path('lspci')
    if lspci:
        (rc, pcidata, err) = self.module.run_command([lspci, '-D'], errors='surrogate_then_replace')
    else:
        pcidata = None
    try:
        block_devs = os.listdir('/sys/block')
    except OSError:
        return device_facts
    devs_wwn = {
        
    }
    try:
        devs_by_id = os.listdir('/dev/disk/by-id')
    except OSError:
        pass
    else:
        for link_name in devs_by_id:
            if link_name.startswith('wwn-'):
                try:
                    wwn_link = os.readlink(os.path.join('/dev/disk/by-id', link_name))
                except OSError:
                    continue
                devs_wwn[os.path.basename(wwn_link)] = link_name[4:]
    links = self.get_all_device_links()
    device_facts['device_links'] = links
    for block in block_devs:
        virtual = 1
        sysfs_no_links = 0
        try:
            path = os.readlink(os.path.join('/sys/block/', block))
        except OSError:
            e = sys.exc_info()[1]
            if (e.errno == errno.EINVAL):
                path = block
                sysfs_no_links = 1
            else:
                continue
        sysdir = os.path.join('/sys/block', path)
        if (sysfs_no_links == 1):
            for folder in os.listdir(sysdir):
                if ('device' in folder):
                    virtual = 0
                    break
        d = {
            
        }
        d['virtual'] = virtual
        d['links'] = {
            
        }
        for (link_type, link_values) in iteritems(links):
            d['links'][link_type] = link_values.get(block, [])
        diskname = os.path.basename(sysdir)
        for key in ['vendor', 'model', 'sas_address', 'sas_device_handle']:
            d[key] = get_file_content(((sysdir + '/device/') + key))
        sg_inq = self.module.get_bin_path('sg_inq')
        if sg_inq:
            device = ('/dev/%s' % block)
            (rc, drivedata, err) = self.module.run_command([sg_inq, device])
            if (rc == 0):
                serial = re.search('Unit serial number:\\s+(\\w+)', drivedata)
                if serial:
                    d['serial'] = serial.group(1)
        for key in ['vendor', 'model']:
            d[key] = get_file_content(((sysdir + '/device/') + key))
        for (key, test) in [('removable', '/removable'), ('support_discard', '/queue/discard_granularity')]:
            d[key] = get_file_content((sysdir + test))
        if (diskname in devs_wwn):
            d['wwn'] = devs_wwn[diskname]
        d['partitions'] = {
            
        }
        for folder in os.listdir(sysdir):
            m = re.search((('(' + diskname) + '\\d+)'), folder)
            if m:
                part = {
                    
                }
                partname = m.group(1)
                part_sysdir = ((sysdir + '/') + partname)
                part['links'] = {
                    
                }
                for (link_type, link_values) in iteritems(links):
                    part['links'][link_type] = link_values.get(partname, [])
                part['start'] = get_file_content((part_sysdir + '/start'), 0)
                part['sectors'] = get_file_content((part_sysdir + '/size'), 0)
                part['sectorsize'] = get_file_content((part_sysdir + '/queue/logical_block_size'))
                if (not part['sectorsize']):
                    part['sectorsize'] = get_file_content((part_sysdir + '/queue/hw_sector_size'), 512)
                part['size'] = bytes_to_human((float(part['sectors']) * 512.0))
                part['uuid'] = get_partition_uuid(partname)
                self.get_holders(part, part_sysdir)
                d['partitions'][partname] = part
        d['rotational'] = get_file_content((sysdir + '/queue/rotational'))
        d['scheduler_mode'] = ''
        scheduler = get_file_content((sysdir + '/queue/scheduler'))
        if (scheduler is not None):
            m = re.match('.*?(\\[(.*)\\])', scheduler)
            if m:
                d['scheduler_mode'] = m.group(2)
        d['sectors'] = get_file_content((sysdir + '/size'))
        if (not d['sectors']):
            d['sectors'] = 0
        d['sectorsize'] = get_file_content((sysdir + '/queue/logical_block_size'))
        if (not d['sectorsize']):
            d['sectorsize'] = get_file_content((sysdir + '/queue/hw_sector_size'), 512)
        d['size'] = bytes_to_human((float(d['sectors']) * 512.0))
        d['host'] = ''
        m = re.match('.+/([a-f0-9]{4}:[a-f0-9]{2}:[0|1][a-f0-9]\\.[0-7])/', sysdir)
        if (m and pcidata):
            pciid = m.group(1)
            did = re.escape(pciid)
            m = re.search((('^' + did) + '\\s(.*)$'), pcidata, re.MULTILINE)
            if m:
                d['host'] = m.group(1)
        self.get_holders(d, sysdir)
        device_facts['devices'][diskname] = d
    return device_facts
