def check_params(self):
    'Check all input params'
    rollback_info = self.rollback_info['RollBackInfos']
    if self.commit_id:
        if (not self.commit_id.isdigit()):
            self.module.fail_json(msg='Error: The parameter of commit_id is invalid.')
        info_bool = False
        for info in rollback_info:
            if (info.get('commitId') == self.commit_id):
                info_bool = True
        if (not info_bool):
            self.module.fail_json(msg='Error: The parameter of commit_id is not exist.')
        if (self.action == 'clear'):
            info_bool = False
            for info in rollback_info:
                if (info.get('commitId') == self.commit_id):
                    if (info.get('userLabel') == '-'):
                        info_bool = True
            if info_bool:
                self.module.fail_json(msg='Error: This commit_id does not have a label.')
    if self.filename:
        if (not self.get_filename_type(self.filename)):
            self.module.fail_json(msg='Error: Invalid file name or file name extension ( *.cfg, *.zip, *.dat ).')
    if self.last:
        if (not self.last.isdigit()):
            self.module.fail_json(msg='Error: Number of configuration checkpoints is not digit.')
        if ((int(self.last) <= 0) or (int(self.last) > 80)):
            self.module.fail_json(msg='Error: Number of configuration checkpoints is not in the range from 1 to 80.')
    if self.oldest:
        if (not self.oldest.isdigit()):
            self.module.fail_json(msg='Error: Number of configuration checkpoints is not digit.')
        if ((int(self.oldest) <= 0) or (int(self.oldest) > 80)):
            self.module.fail_json(msg='Error: Number of configuration checkpoints is not in the range from 1 to 80.')
    if self.label:
        if self.label[0].isdigit():
            self.module.fail_json(msg='Error: Commit label which should not start with a number.')
        if (len(self.label.replace(' ', '')) == 1):
            if (self.label == '-'):
                self.module.fail_json(msg='Error: Commit label which should not be "-"')
        if ((len(self.label.replace(' ', '')) < 1) or (len(self.label) > 256)):
            self.module.fail_json(msg='Error: Label of configuration checkpoints is a string of 1 to 256 characters.')
        if (self.action == 'rollback'):
            info_bool = False
            for info in rollback_info:
                if (info.get('userLabel') == self.label):
                    info_bool = True
            if (not info_bool):
                self.module.fail_json(msg='Error: The parameter of userLabel is not exist.')
        if (self.action == 'commit'):
            info_bool = False
            for info in rollback_info:
                if (info.get('userLabel') == self.label):
                    info_bool = True
            if info_bool:
                self.module.fail_json(msg='Error: The parameter of userLabel is existing.')
        if (self.action == 'set'):
            info_bool = False
            for info in rollback_info:
                if (info.get('commitId') == self.commit_id):
                    if (info.get('userLabel') != '-'):
                        info_bool = True
            if info_bool:
                self.module.fail_json(msg='Error: The userLabel of this commitid is present and can be reset after deletion.')