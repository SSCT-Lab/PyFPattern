def get_vars_files(self):
    if (self.vars_files is None):
        return []
    elif (not isinstance(self.vars_files, list)):
        return [self.vars_files]
    return self.vars_files