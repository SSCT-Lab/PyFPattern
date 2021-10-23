def choosepath(self, print_result=True):
    if (not self.paths):
        if (self.fallback_inc and (not self.inc_dir)):
            self.inc_dir = self.fallback_inc[0]
        if (self.fallback_lib and (not self.lib_dir)):
            self.lib_dir = self.fallback_lib[0]
            self.libs[0] = os.path.splitext(self.fallback_lib[2])[0]
        if (self.inc_dir and self.lib_dir):
            if print_result:
                print(('Path for %s found.' % self.name))
            return True
        if print_result:
            print(('Path for %s not found.' % self.name))
            for info in self.prune_info:
                print(info)
            if self.required:
                print('Too bad that is a requirement! Hand-fix the "Setup"')
        return False
    elif (len(self.paths) == 1):
        self.path = self.paths[0]
        if print_result:
            print(('Path for %s: %s' % (self.name, self.path)))
    else:
        logging.warning('Multiple paths to choose from:%s', self.paths)
        self.path = self.paths[0]
        if print_result:
            print(('Path for %s: %s' % (self.name, self.path)))
    return True