

def get_lvm_facts(self):
    ' Get LVM Facts if running as root and lvm utils are available '
    lvm_facts = {
        
    }
    if ((os.getuid() == 0) and self.module.get_bin_path('vgs')):
        lvm_util_options = '--noheadings --nosuffix --units g --separator ,'
        vgs_path = self.module.get_bin_path('vgs')
        vgs = {
            
        }
        if vgs_path:
            (rc, vg_lines, err) = self.module.run_command(('%s %s' % (vgs_path, lvm_util_options)))
            for vg_line in vg_lines.splitlines():
                items = vg_line.split(',')
                vgs[items[0]] = {
                    'size_g': items[(- 2)],
                    'free_g': items[(- 1)],
                    'num_lvs': items[2],
                    'num_pvs': items[1],
                }
        lvs_path = self.module.get_bin_path('lvs')
        lvs = {
            
        }
        if lvs_path:
            (rc, lv_lines, err) = self.module.run_command(('%s %s' % (lvs_path, lvm_util_options)))
            for lv_line in lv_lines.splitlines():
                items = lv_line.split(',')
                lvs[items[0]] = {
                    'size_g': items[3],
                    'vg': items[1],
                }
        pvs_path = self.module.get_bin_path('pvs')
        pvs = {
            
        }
        if pvs_path:
            (rc, pv_lines, err) = self.module.run_command(('%s %s' % (pvs_path, lvm_util_options)))
            for pv_line in pv_lines.splitlines():
                items = pv_line.split(',')
                pvs[self._find_mapper_device_name(items[0])] = {
                    'size_g': items[4],
                    'free_g': items[5],
                    'vg': items[1],
                }
        lvm_facts['lvm'] = {
            'lvs': lvs,
            'vgs': vgs,
            'pvs': pvs,
        }
    return lvm_facts
