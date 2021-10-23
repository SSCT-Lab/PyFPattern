def main():
    module = AnsibleModule(argument_spec=dict(paths=dict(type='list', required=True, aliases=['name', 'path']), patterns=dict(type='list', default=['*'], aliases=['pattern']), excludes=dict(type='list', aliases=['exclude']), contains=dict(type='str'), file_type=dict(type='str', default='file', choices=['any', 'directory', 'file', 'link']), age=dict(type='str'), age_stamp=dict(type='str', default='mtime', choices=['atime', 'mtime', 'ctime']), size=dict(type='str'), recurse=dict(type='bool', default='no'), hidden=dict(type='bool', default='no'), follow=dict(type='bool', default='no'), get_checksum=dict(type='bool', default='no'), use_regex=dict(type='bool', default='no'), depth=dict(type='int', default=None)), supports_check_mode=True)
    params = module.params
    filelist = []
    if (params['age'] is None):
        age = None
    else:
        m = re.match('^(-?\\d+)(s|m|h|d|w)?$', params['age'].lower())
        seconds_per_unit = {
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800,
        }
        if m:
            age = (int(m.group(1)) * seconds_per_unit.get(m.group(2), 1))
        else:
            module.fail_json(age=params['age'], msg='failed to process age')
    if (params['size'] is None):
        size = None
    else:
        m = re.match('^(-?\\d+)(b|k|m|g|t)?$', params['size'].lower())
        bytes_per_unit = {
            'b': 1,
            'k': 1024,
            'm': (1024 ** 2),
            'g': (1024 ** 3),
            't': (1024 ** 4),
        }
        if m:
            size = (int(m.group(1)) * bytes_per_unit.get(m.group(2), 1))
        else:
            module.fail_json(size=params['size'], msg='failed to process size')
    now = time.time()
    msg = ''
    looked = 0
    for npath in params['paths']:
        npath = os.path.expanduser(os.path.expandvars(npath))
        if os.path.isdir(npath):
            ' ignore followlinks for python version < 2.6 '
            for (root, dirs, files) in (((sys.version_info < (2, 6, 0)) and os.walk(npath)) or os.walk(npath, followlinks=params['follow'])):
                if params['depth']:
                    depth = root.replace(npath.rstrip(os.path.sep), '').count(os.path.sep)
                    if (files or dirs):
                        depth += 1
                    if (depth > params['depth']):
                        del dirs[:]
                        continue
                looked = ((looked + len(files)) + len(dirs))
                for fsobj in (files + dirs):
                    fsname = os.path.normpath(os.path.join(root, fsobj))
                    if (os.path.basename(fsname).startswith('.') and (not params['hidden'])):
                        continue
                    try:
                        st = os.lstat(fsname)
                    except:
                        msg += ('%s was skipped as it does not seem to be a valid file or it cannot be accessed\n' % fsname)
                        continue
                    r = {
                        'path': fsname,
                    }
                    if (params['file_type'] == 'any'):
                        if (pfilter(fsobj, params['patterns'], params['excludes'], params['use_regex']) and agefilter(st, now, age, params['age_stamp'])):
                            r.update(statinfo(st))
                            filelist.append(r)
                    elif (stat.S_ISDIR(st.st_mode) and (params['file_type'] == 'directory')):
                        if (pfilter(fsobj, params['patterns'], params['excludes'], params['use_regex']) and agefilter(st, now, age, params['age_stamp'])):
                            r.update(statinfo(st))
                            filelist.append(r)
                    elif (stat.S_ISREG(st.st_mode) and (params['file_type'] == 'file')):
                        if (pfilter(fsobj, params['patterns'], params['excludes'], params['use_regex']) and agefilter(st, now, age, params['age_stamp']) and sizefilter(st, size) and contentfilter(fsname, params['contains'])):
                            r.update(statinfo(st))
                            if params['get_checksum']:
                                r['checksum'] = module.sha1(fsname)
                            filelist.append(r)
                    elif (stat.S_ISLNK(st.st_mode) and (params['file_type'] == 'link')):
                        if (pfilter(fsobj, params['patterns'], params['excludes'], params['use_regex']) and agefilter(st, now, age, params['age_stamp'])):
                            r.update(statinfo(st))
                            filelist.append(r)
                if (not params['recurse']):
                    break
        else:
            msg += ('%s was skipped as it does not seem to be a valid directory or it cannot be accessed\n' % npath)
    matched = len(filelist)
    module.exit_json(files=filelist, changed=False, msg=msg, matched=matched, examined=looked)