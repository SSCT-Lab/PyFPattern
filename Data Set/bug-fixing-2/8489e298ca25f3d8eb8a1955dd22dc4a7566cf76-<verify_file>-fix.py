

def verify_file(self, path):
    ' Verify if file is usable by this plugin, base does minimal accessibility check '
    valid = super(InventoryModule, self).verify_file(path)
    if valid:
        shebang_present = False
        try:
            with open(path, 'rb') as inv_file:
                initial_chars = inv_file.read(2)
                if initial_chars.startswith(b'#!'):
                    shebang_present = True
        except:
            pass
        if ((not os.access(path, os.X_OK)) and (not shebang_present)):
            valid = False
    return valid
