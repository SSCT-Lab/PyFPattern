def save_configuration(self):
    url = self.host.configManager.firmwareSystem.BackupFirmwareConfiguration()
    url = url.replace('*', self.host.name)
    if os.path.isdir(self.dest):
        filename = url.rsplit('/', 1)[1]
        self.dest = os.path.join(self.dest, filename)
    else:
        (filename, file_extension) = os.path.splitext(self.dest)
        if (file_extension != '.tgz'):
            self.dest = (filename + '.tgz')
    try:
        request = open_url(url=url, validate_certs=self.validate_certs)
        with open(self.dest, 'wb') as file:
            file.write(request.read())
        self.module.exit_json(changed=True, dest_file=self.dest)
    except IOError as e:
        self.module.fail_json(msg=('Failed to write backup file. Ensure that the dest path exists and is writable. Details : %s' % to_native(e)))
    except Exception as e:
        self.module.fail_json(msg=to_native(e))