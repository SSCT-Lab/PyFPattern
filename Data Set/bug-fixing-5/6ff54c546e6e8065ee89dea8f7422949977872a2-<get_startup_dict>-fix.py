def get_startup_dict(self):
    'Retrieves the current config from the device or cache\n        '
    cmd = 'display startup'
    (rc, out, err) = exec_command(self.module, cmd)
    if (rc != 0):
        self.module.fail_json(msg=err)
    cfg = str(out).strip()
    startup_info = dict()
    startup_info['StartupInfos'] = list()
    if (not cfg):
        return startup_info
    else:
        re_find = re.findall('(.*)\\s*\\s*Configured\\s*startup\\s*system\\s*software:\\s*(.*)\\s*Startup\\s*system\\s*software:\\s*(.*)\\s*Next\\s*startup\\s*system\\s*software:\\s*(.*)\\s*Startup\\s*saved-configuration\\s*file:\\s*(.*)\\s*Next\\s*startup\\s*saved-configuration\\s*file:\\s*(.*)\\s*Startup\\s*paf\\s*file:\\s*(.*)\\s*Next\\s*startup\\s*paf\\s*file:\\s*(.*)\\s*Startup\\s*patch\\s*package:\\s*(.*)\\s*Next\\s*startup\\s*patch\\s*package:\\s*(.*)', cfg)
        if re_find:
            for mem in re_find:
                startup_info['StartupInfos'].append(dict(nextStartupFile=mem[5], configSysSoft=mem[1], curentSysSoft=mem[2], nextSysSoft=mem[3], curentStartupFile=mem[4], curentPatchFile=mem[8], nextPatchFile=mem[9], postion=mem[0]))
            return startup_info
        return startup_info