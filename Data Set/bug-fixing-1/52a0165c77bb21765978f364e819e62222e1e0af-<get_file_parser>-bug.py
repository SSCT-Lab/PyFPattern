

def get_file_parser(hostsfile, groups, loader):
    shebang_present = False
    processed = False
    myerr = []
    parser = None
    try:
        inv_file = open(hostsfile)
        first_line = inv_file.readlines()[0]
        inv_file.close()
        if first_line.startswith('#!'):
            shebang_present = True
    except:
        pass
    if loader.is_executable(hostsfile):
        try:
            parser = InventoryScript(loader=loader, groups=groups, filename=hostsfile)
            processed = True
        except Exception as e:
            myerr.append(str(e))
    elif shebang_present:
        myerr.append(('The file %s looks like it should be an executable inventory script, but is not marked executable. Perhaps you want to correct this with `chmod +x %s`?' % (hostsfile, hostsfile)))
    if ((not processed) and (os.path.splitext(hostsfile)[(- 1)] in C.YAML_FILENAME_EXTENSIONS)):
        try:
            parser = InventoryYAMLParser(loader=loader, groups=groups, filename=hostsfile)
            processed = True
        except Exception as e:
            myerr.append(str(e))
    if (not processed):
        try:
            parser = InventoryINIParser(loader=loader, groups=groups, filename=hostsfile)
            processed = True
        except Exception as e:
            myerr.append(str(e))
    if ((not processed) and myerr):
        raise AnsibleError('\n'.join(myerr))
    return parser
