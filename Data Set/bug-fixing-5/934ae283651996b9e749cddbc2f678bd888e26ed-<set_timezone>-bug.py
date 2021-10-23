def set_timezone(self, value):
    self._edit_file(filename=self.conf_files['name'], regexp=self.regexps['name'], value=(self.tzline_format % value))
    self.execute(self.update_timezone)