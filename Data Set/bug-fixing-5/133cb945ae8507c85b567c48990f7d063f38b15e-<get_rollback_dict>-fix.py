def get_rollback_dict(self):
    ' get rollback attributes dict.'
    rollback_info = dict()
    rollback_info['RollBackInfos'] = list()
    flags = list()
    exp = 'commit list'
    flags.append(exp)
    cfg_info = self.get_config(flags)
    if (not cfg_info):
        return rollback_info
    cfg_line = cfg_info.split('\n')
    for cfg in cfg_line:
        if re.findall('^\\d', cfg):
            pre_rollback_info = cfg.split()
            rollback_info['RollBackInfos'].append(dict(commitId=pre_rollback_info[1], userLabel=pre_rollback_info[2]))
    return rollback_info