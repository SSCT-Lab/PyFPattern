def get_rollback_dict(self):
    ' get rollback attributes dict.'
    rollback_info = dict()
    conf_str = CE_NC_GET_CHECKPOINT
    xml_str = get_nc_config(self.module, conf_str)
    rollback_info['RollBackInfos'] = list()
    if ('<data/>' in xml_str):
        return rollback_info
    else:
        re_find = re.findall('.*<commitId>(.*)</commitId>.*\\s*<userName>(.*)</userName>.*\\s*<userLabel>(.*)</userLabel>.*', xml_str)
        for mem in re_find:
            rollback_info['RollBackInfos'].append(dict(commitId=mem[0], userLabel=mem[2]))
        return rollback_info