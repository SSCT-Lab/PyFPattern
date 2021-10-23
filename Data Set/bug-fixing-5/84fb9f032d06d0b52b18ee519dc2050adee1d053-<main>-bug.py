def main():
    module = AnsibleModule(argument_spec=dict(path=dict(required=True, type='path'), follow=dict(type='bool', default='no'), get_md5=dict(type='bool', default='yes'), get_checksum=dict(type='bool', default='yes'), get_mime=dict(type='bool', default='yes', aliases=['mime', 'mime_type', 'mime-type']), get_attributes=dict(type='bool', default='yes', aliases=['attr', 'attributes']), checksum_algorithm=dict(type='str', default='sha1', choices=['sha1', 'sha224', 'sha256', 'sha384', 'sha512'], aliases=['checksum', 'checksum_algo'])), supports_check_mode=True)
    path = module.params.get('path')
    b_path = to_bytes(path, errors='surrogate_or_strict')
    follow = module.params.get('follow')
    get_mime = module.params.get('get_mime')
    get_attr = module.params.get('get_attributes')
    get_md5 = module.params.get('get_md5')
    get_checksum = module.params.get('get_checksum')
    checksum_algorithm = module.params.get('checksum_algorithm')
    try:
        if follow:
            st = os.stat(b_path)
        else:
            st = os.lstat(b_path)
    except OSError:
        e = get_exception()
        if (e.errno == errno.ENOENT):
            output = {
                'exists': False,
            }
            module.exit_json(changed=False, stat=output)
        module.fail_json(msg=e.strerror)
    output = format_output(module, path, st)
    for perm in [('readable', os.R_OK), ('writeable', os.W_OK), ('executable', os.X_OK)]:
        output[perm[0]] = os.access(b_path, perm[1])
    if output.get('islnk'):
        output['lnk_source'] = os.path.realpath(b_path)
    try:
        pw = pwd.getpwuid(st.st_uid)
        output['pw_name'] = pw.pw_name
    except:
        pass
    try:
        grp_info = grp.getgrgid(st.st_gid)
        output['gr_name'] = grp_info.gr_name
    except:
        pass
    if (output.get('isreg') and output.get('readable')):
        if get_md5:
            try:
                output['md5'] = module.md5(b_path)
            except ValueError:
                output['md5'] = None
        if get_checksum:
            output['checksum'] = module.digest_from_file(b_path, checksum_algorithm)
    if get_mime:
        output['mimetype'] = output['charset'] = 'unknown'
        mimecmd = module.get_bin_path('file')
        if mimecmd:
            mimecmd = [mimecmd, '-i', b_path]
            try:
                (rc, out, err) = module.run_command(mimecmd)
                if (rc == 0):
                    (mimetype, charset) = out.split(':')[1].split(';')
                    output['mimetype'] = mimetype.strip()
                    output['charset'] = charset.split('=')[1].strip()
            except:
                pass
    if get_attr:
        output['version'] = None
        output['attributes'] = []
        output['attr_flags'] = ''
        out = module.get_file_attributes(b_path)
        for x in ('version', 'attributes', 'attr_flags'):
            if (x in out):
                output[x] = out[x]
    module.exit_json(changed=False, stat=output)