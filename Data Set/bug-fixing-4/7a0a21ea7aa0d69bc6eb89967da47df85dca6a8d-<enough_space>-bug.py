def enough_space(self):
    'Whether device has enough space'
    commands = list()
    cmd = ('dir %s' % self.file_system)
    commands.append(cmd)
    output = run_commands(self.module, commands)
    if (not output):
        return True
    match = re.search('\\((.*) KB free\\)', output[0])
    kbytes_free = match.group(1)
    kbytes_free = kbytes_free.replace(',', '')
    file_size = os.path.getsize(self.local_file)
    if ((int(kbytes_free) * 1024) > file_size):
        return True
    return False