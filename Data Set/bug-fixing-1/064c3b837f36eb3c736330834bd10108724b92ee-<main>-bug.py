

def main():
    argument_spec = url_argument_spec()
    argument_spec.update(url=dict(type='str', required=True), dest=dict(type='path', required=True), backup=dict(type='bool'), sha256sum=dict(type='str', default=''), checksum=dict(type='str', default=''), timeout=dict(type='int', default=10), headers=dict(type='str'), tmp_dest=dict(type='path'))
    module = AnsibleModule(argument_spec=argument_spec, add_file_common_args=True, supports_check_mode=True, mutually_exclusive=['checksum', 'sha256sum'])
    url = module.params['url']
    dest = module.params['dest']
    backup = module.params['backup']
    force = module.params['force']
    sha256sum = module.params['sha256sum']
    checksum = module.params['checksum']
    use_proxy = module.params['use_proxy']
    timeout = module.params['timeout']
    tmp_dest = module.params['tmp_dest']
    if module.params['headers']:
        try:
            headers = dict((item.split(':', 1) for item in module.params['headers'].split(',')))
        except:
            module.fail_json(msg='The header parameter requires a key:value,key:value syntax to be properly parsed.')
    else:
        headers = None
    dest_is_dir = os.path.isdir(dest)
    last_mod_time = None
    if sha256sum:
        checksum = ('sha256:%s' % sha256sum)
    if checksum:
        try:
            (algorithm, checksum) = checksum.rsplit(':', 1)
            checksum = re.sub('\\W+', '', checksum).lower()
            int(checksum, 16)
        except ValueError:
            module.fail_json(msg='The checksum parameter has to be in format <algorithm>:<checksum>')
    if ((not dest_is_dir) and os.path.exists(dest)):
        checksum_mismatch = False
        if ((not force) and (checksum != '')):
            destination_checksum = module.digest_from_file(dest, algorithm)
            if (checksum == destination_checksum):
                module.exit_json(msg='file already exists', dest=dest, url=url, changed=False)
            checksum_mismatch = True
        if ((not force) and (not checksum_mismatch)):
            module.params['path'] = dest
            file_args = module.load_file_common_arguments(module.params)
            file_args['path'] = dest
            changed = module.set_fs_attributes_if_different(file_args, False)
            if changed:
                module.exit_json(msg='file already exists but file attributes changed', dest=dest, url=url, changed=changed)
            module.exit_json(msg='file already exists', dest=dest, url=url, changed=changed)
        mtime = os.path.getmtime(dest)
        last_mod_time = datetime.datetime.utcfromtimestamp(mtime)
        if checksum_mismatch:
            force = True
    (tmpsrc, info) = url_get(module, url, dest, use_proxy, last_mod_time, force, timeout, headers, tmp_dest)
    if dest_is_dir:
        filename = extract_filename_from_headers(info)
        if (not filename):
            filename = url_filename(info['url'])
        dest = os.path.join(dest, filename)
    checksum_src = None
    checksum_dest = None
    if module.check_mode:
        os.remove(tmpsrc)
        res_args = dict(url=url, dest=dest, src=tmpsrc, changed=True, msg=info.get('msg', ''))
        module.exit_json(**res_args)
    if (not os.path.exists(tmpsrc)):
        os.remove(tmpsrc)
        module.fail_json(msg='Request failed', status_code=info['status'], response=info['msg'])
    if (not os.access(tmpsrc, os.R_OK)):
        os.remove(tmpsrc)
        module.fail_json(msg=('Source %s not readable' % tmpsrc))
    checksum_src = module.sha1(tmpsrc)
    if os.path.exists(dest):
        if (not os.access(dest, os.W_OK)):
            os.remove(tmpsrc)
            module.fail_json(msg=('Destination %s not writable' % dest))
        if (not os.access(dest, os.R_OK)):
            os.remove(tmpsrc)
            module.fail_json(msg=('Destination %s not readable' % dest))
        checksum_dest = module.sha1(dest)
    elif (not os.access(os.path.dirname(dest), os.W_OK)):
        os.remove(tmpsrc)
        module.fail_json(msg=('Destination %s not writable' % os.path.dirname(dest)))
    backup_file = None
    if (checksum_src != checksum_dest):
        try:
            if backup:
                if os.path.exists(dest):
                    backup_file = module.backup_local(dest)
            module.atomic_move(tmpsrc, dest)
        except Exception as e:
            if os.path.exists(tmpsrc):
                os.remove(tmpsrc)
            module.fail_json(msg=('failed to copy %s to %s: %s' % (tmpsrc, dest, to_native(e))), exception=traceback.format_exc())
        changed = True
    else:
        changed = False
    if (checksum != ''):
        destination_checksum = module.digest_from_file(dest, algorithm)
        if (checksum != destination_checksum):
            os.remove(dest)
            module.fail_json(msg=('The checksum for %s did not match %s; it was %s.' % (dest, checksum, destination_checksum)))
    module.params['path'] = dest
    file_args = module.load_file_common_arguments(module.params)
    file_args['path'] = dest
    changed = module.set_fs_attributes_if_different(file_args, changed)
    try:
        md5sum = module.md5(dest)
    except ValueError:
        md5sum = None
    res_args = dict(url=url, dest=dest, src=tmpsrc, md5sum=md5sum, checksum_src=checksum_src, checksum_dest=checksum_dest, changed=changed, msg=info.get('msg', ''), status_code=info.get('status', ''))
    if backup_file:
        res_args['backup_file'] = backup_file
    module.exit_json(**res_args)
