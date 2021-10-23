def get_startup_dict(self):
    ' get rollback attributes dict.'
    startup_info = dict()
    conf_str = CE_NC_GET_STARTUP_INFO
    xml_str = get_nc_config(self.module, conf_str)
    startup_info['StartupInfos'] = list()
    if ('<data/>' in xml_str):
        return startup_info
    else:
        re_find = re.findall('.*<position>(.*)</position>.*\\s*<nextStartupFile>(.*)</nextStartupFile>.*\\s*<configedSysSoft>(.*)</configedSysSoft>.*\\s*<curSysSoft>(.*)</curSysSoft>.*\\s*<nextSysSoft>(.*)</nextSysSoft>.*\\s*<curStartupFile>(.*)</curStartupFile>.*\\s*<curPatchFile>(.*)</curPatchFile>.*\\s*<nextPatchFile>(.*)</nextPatchFile>.*', xml_str)
        for mem in re_find:
            startup_info['StartupInfos'].append(dict(position=mem[0], nextStartupFile=mem[1], configSysSoft=mem[2], curentSysSoft=mem[3], nextSysSoft=mem[4], curentStartupFile=mem[5], curentPatchFile=mem[6], nextPatchFile=mem[7]))
        return startup_info