def merge_syslog_logfile(self):
    'config logfile'
    logfile_max_num = '200'
    conf_str = CE_NC_MERGE_LOG_FILE_INFO_HEADER
    if self.logfile_max_num:
        if (self.state == 'present'):
            logfile_max_num = self.logfile_max_num
        elif ((self.logfile_max_num != '200') and (self.cur_logfile_info['maxFileNum'] == self.logfile_max_num)):
            logfile_max_num = '200'
        conf_str += ('<maxFileNum>%s</maxFileNum>' % logfile_max_num)
    if self.logfile_max_size:
        logfile_max_size = '32'
        if (self.state == 'present'):
            logfile_max_size = self.logfile_max_size
        elif ((self.logfile_max_size != '32') and (self.cur_logfile_info['maxFileSize'] == self.logfile_max_size)):
            logfile_max_size = '32'
        conf_str += ('<maxFileSize>%s</maxFileSize>' % logfile_max_size)
    conf_str += '<logFileType>log</logFileType>'
    conf_str += CE_NC_MERGE_LOG_FILE_INFO_TAIL
    if (self.state == 'present'):
        if self.logfile_max_num:
            if (self.cur_logfile_info['maxFileNum'] != self.logfile_max_num):
                cmd = ('info-center max-logfile-number %s' % self.logfile_max_num)
                self.updates_cmd.append(cmd)
                self.changed = True
        if self.logfile_max_size:
            if (self.cur_logfile_info['maxFileSize'] != self.logfile_max_size):
                cmd = ('info-center logfile size %s' % self.logfile_max_size)
                self.updates_cmd.append(cmd)
                self.changed = True
    if (self.state == 'absent'):
        if (self.logfile_max_num and (self.logfile_max_num != '200')):
            if (self.cur_logfile_info['maxFileNum'] == self.logfile_max_num):
                cmd = 'undo info-center max-logfile-number'
                self.updates_cmd.append(cmd)
                self.changed = True
        if (self.logfile_max_size and (self.logfile_max_size != '32')):
            if (self.cur_logfile_info['maxFileSize'] == self.logfile_max_size):
                cmd = 'undo info-center logfile size'
                self.updates_cmd.append(cmd)
                self.changed = True
    if self.changed:
        recv_xml = set_nc_config(self.module, conf_str)
        if ('<ok/>' not in recv_xml):
            self.module.fail_json(msg='Error: Merge syslog logfile failed.')