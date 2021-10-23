def main():
    module = AnsibleModule(argument_spec=dict(path=dict(required=True, aliases=['dest', 'destfile', 'name'], type='path'), state=dict(default='present', choices=['absent', 'present']), marker=dict(default='# {mark} ANSIBLE MANAGED BLOCK', type='str'), block=dict(default='', type='str', aliases=['content']), insertafter=dict(default=None), insertbefore=dict(default=None), create=dict(default=False, type='bool'), backup=dict(default=False, type='bool'), validate=dict(default=None, type='str')), mutually_exclusive=[['insertbefore', 'insertafter']], add_file_common_args=True, supports_check_mode=True)
    params = module.params
    path = params['path']
    if module.boolean(params.get('follow', None)):
        path = os.path.realpath(path)
    if os.path.isdir(path):
        module.fail_json(rc=256, msg=('Path %s is a directory !' % path))
    path_exists = os.path.exists(path)
    if (not path_exists):
        if (not module.boolean(params['create'])):
            module.fail_json(rc=257, msg=('Path %s does not exist !' % path))
        original = None
        lines = []
    else:
        f = open(path, 'rb')
        original = f.read()
        f.close()
        lines = original.splitlines()
    diff = {
        'before': '',
        'after': '',
        'before_header': ('%s (content)' % path),
        'after_header': ('%s (content)' % path),
    }
    if (module._diff and original):
        diff['before'] = original
    insertbefore = params['insertbefore']
    insertafter = params['insertafter']
    block = to_bytes(params['block'])
    marker = to_bytes(params['marker'])
    present = (params['state'] == 'present')
    if ((not present) and (not path_exists)):
        module.exit_json(changed=False, msg=('File %s not present' % path))
    if ((insertbefore is None) and (insertafter is None)):
        insertafter = 'EOF'
    if (insertafter not in (None, 'EOF')):
        insertre = re.compile(insertafter)
    elif (insertbefore not in (None, 'BOF')):
        insertre = re.compile(insertbefore)
    else:
        insertre = None
    marker0 = re.sub(b('{mark}'), b('BEGIN'), marker)
    marker1 = re.sub(b('{mark}'), b('END'), marker)
    if (present and block):
        if module.ansible_version.startswith('1.'):
            block = re.sub('', block, '')
        blocklines = (([marker0] + block.splitlines()) + [marker1])
    else:
        blocklines = []
    n0 = n1 = None
    for (i, line) in enumerate(lines):
        if (line == marker0):
            n0 = i
        if (line == marker1):
            n1 = i
    if (None in (n0, n1)):
        n0 = None
        if (insertre is not None):
            for (i, line) in enumerate(lines):
                if insertre.search(line):
                    n0 = i
            if (n0 is None):
                n0 = len(lines)
            elif (insertafter is not None):
                n0 += 1
        elif (insertbefore is not None):
            n0 = 0
        else:
            n0 = len(lines)
    elif (n0 < n1):
        lines[n0:(n1 + 1)] = []
    else:
        lines[n1:(n0 + 1)] = []
        n0 = n1
    lines[n0:n0] = blocklines
    if lines:
        result = b('\n').join(lines)
        if ((original is None) or original.endswith(b('\n'))):
            result += b('\n')
    else:
        result = ''
    if module._diff:
        diff['after'] = result
    if (original == result):
        msg = ''
        changed = False
    elif (original is None):
        msg = 'File created'
        changed = True
    elif (not blocklines):
        msg = 'Block removed'
        changed = True
    else:
        msg = 'Block inserted'
        changed = True
    if (changed and (not module.check_mode)):
        if (module.boolean(params['backup']) and path_exists):
            module.backup_local(path)
        write_changes(module, result, path)
    if (module.check_mode and (not path_exists)):
        module.exit_json(changed=changed, msg=msg, diff=diff)
    attr_diff = {
        
    }
    (msg, changed) = check_file_attrs(module, changed, msg, attr_diff)
    attr_diff['before_header'] = ('%s (file attributes)' % path)
    attr_diff['after_header'] = ('%s (file attributes)' % path)
    difflist = [diff, attr_diff]
    module.exit_json(changed=changed, msg=msg, diff=difflist)