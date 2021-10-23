def process(self):
    self.platform = get_platform().lower()
    self.args['name'] = self.args['name'].strip()
    self.args['value'] = self._parse_value(self.args['value'])
    thisname = self.args['name']
    self.proc_value = self.get_token_curr_value(thisname)
    self.read_sysctl_file()
    if (thisname not in self.file_values):
        self.file_values[thisname] = None
    self.fix_lines()
    if ((self.file_values[thisname] is None) and (self.args['state'] == 'present')):
        self.changed = True
        self.write_file = True
    elif ((self.file_values[thisname] is None) and (self.args['state'] == 'absent')):
        self.changed = False
    elif (self.file_values[thisname] != self.args['value']):
        self.changed = True
        self.write_file = True
    if self.args['sysctl_set']:
        if (self.proc_value is None):
            self.changed = True
        elif (not self._values_is_equal(self.proc_value, self.args['value'])):
            self.changed = True
            self.set_proc = True
    if (not self.module.check_mode):
        if self.write_file:
            self.write_sysctl()
        if (self.write_file and self.args['reload']):
            self.reload_sysctl()
        if self.set_proc:
            self.set_token_value(self.args['name'], self.args['value'])