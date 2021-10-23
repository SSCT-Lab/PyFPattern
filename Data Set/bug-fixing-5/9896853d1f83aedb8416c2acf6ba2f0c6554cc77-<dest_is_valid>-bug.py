def dest_is_valid(self):
    if (not self.check_mode):
        if (not os.path.basename(self.dest)):
            if os.path.isdir(self.dest):
                self.log('Path is dir. Appending blob name.')
                self.dest += self.blob
            else:
                try:
                    self.log('Attempting to makedirs {0}'.format(self.dest))
                    os.makddirs(self.dest)
                except IOError as exc:
                    self.fail('Failed to create directory {0} - {1}'.format(self.dest, str(exc)))
                self.dest += self.blob
        else:
            file_name = os.path.basename(self.dest)
            path = self.dest.replace(file_name, '')
            self.log('Checking path {0}'.format(path))
            if (not os.path.isdir(path)):
                try:
                    self.log('Attempting to makedirs {0}'.format(path))
                    os.makedirs(path)
                except IOError as exc:
                    self.fail('Failed to create directory {0} - {1}'.format(path, str(exc)))
        self.log('Checking final path {0}'.format(self.dest))
        if (os.path.isfile(self.dest) and (not self.force)):
            self.log('Dest {0} already exists. Cannot download. Use the force option.'.format(self.dest))
            return False
    return True