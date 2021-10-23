def main():
    pam_items = ['core', 'data', 'fsize', 'memlock', 'nofile', 'rss', 'stack', 'cpu', 'nproc', 'as', 'maxlogins', 'maxsyslogins', 'priority', 'locks', 'sigpending', 'msgqueue', 'nice', 'rtprio', 'chroot']
    pam_types = ['soft', 'hard', '-']
    limits_conf = '/etc/security/limits.conf'
    module = AnsibleModule(argument_spec=dict(domain=dict(required=True, type='str'), limit_type=dict(required=True, type='str', choices=pam_types), limit_item=dict(required=True, type='str', choices=pam_items), value=dict(required=True, type='str'), use_max=dict(default=False, type='bool'), use_min=dict(default=False, type='bool'), backup=dict(default=False, type='bool'), dest=dict(default=limits_conf, type='str'), comment=dict(required=False, default='', type='str')))
    domain = module.params['domain']
    limit_type = module.params['limit_type']
    limit_item = module.params['limit_item']
    value = module.params['value']
    use_max = module.params['use_max']
    use_min = module.params['use_min']
    backup = module.params['backup']
    limits_conf = module.params['dest']
    new_comment = module.params['comment']
    changed = False
    if os.path.isfile(limits_conf):
        if (not os.access(limits_conf, os.W_OK)):
            module.fail_json(msg=('%s is not writable. Use sudo' % limits_conf))
    else:
        module.fail_json(msg=('%s is not visible (check presence, access rights, use sudo)' % limits_conf))
    if (use_max and use_min):
        module.fail_json(msg='Cannot use use_min and use_max at the same time.')
    if (not ((value in ['unlimited', 'infinity', '-1']) or value.isdigit())):
        module.fail_json(msg="Argument 'value' can be one of 'unlimited', 'infinity', '-1' or positive number. Refer to manual pages for more details.")
    if backup:
        backup_file = module.backup_local(limits_conf)
    space_pattern = re.compile('\\s+')
    message = ''
    f = open(limits_conf, 'rb')
    nf = tempfile.NamedTemporaryFile(mode='w+')
    found = False
    new_value = value
    for line in f:
        line = to_native(line, errors='surrogate_or_strict')
        if line.startswith('#'):
            nf.write(line)
            continue
        newline = re.sub(space_pattern, ' ', line).strip()
        if (not newline):
            nf.write(line)
            continue
        newline = newline.split('#', 1)[0]
        try:
            old_comment = line.split('#', 1)[1]
        except:
            old_comment = ''
        newline = newline.rstrip()
        if (not new_comment):
            new_comment = old_comment
        if new_comment:
            new_comment = ('\t#' + new_comment)
        line_fields = newline.split(' ')
        if (len(line_fields) != 4):
            nf.write(line)
            continue
        line_domain = line_fields[0]
        line_type = line_fields[1]
        line_item = line_fields[2]
        actual_value = line_fields[3]
        if (not ((actual_value in ['unlimited', 'infinity', '-1']) or actual_value.isdigit())):
            module.fail_json(msg=("Invalid configuration of '%s'. Current value of %s is unsupported." % (limits_conf, line_item)))
        if ((line_domain == domain) and (line_type == limit_type) and (line_item == limit_item)):
            found = True
            if (value == actual_value):
                message = line
                nf.write(line)
                continue
            actual_value_unlimited = (actual_value in ['unlimited', 'infinity', '-1'])
            value_unlimited = (value in ['unlimited', 'infinity', '-1'])
            if use_max:
                if (value.isdigit() and actual_value.isdigit()):
                    new_value = str(max(int(value), int(actual_value)))
                elif actual_value_unlimited:
                    new_value = actual_value
                else:
                    new_value = value
            if use_min:
                if (value.isdigit() and actual_value.isdigit()):
                    new_value = str(min(int(value), int(actual_value)))
                elif value_unlimited:
                    new_value = actual_value
                else:
                    new_value = value
            if (new_value != actual_value):
                changed = True
                new_limit = ((((((((domain + '\t') + limit_type) + '\t') + limit_item) + '\t') + new_value) + new_comment) + '\n')
                message = new_limit
                nf.write(new_limit)
            else:
                message = line
                nf.write(line)
        else:
            nf.write(line)
    if (not found):
        changed = True
        new_limit = ((((((((domain + '\t') + limit_type) + '\t') + limit_item) + '\t') + new_value) + new_comment) + '\n')
        message = new_limit
        nf.write(new_limit)
    f.close()
    nf.flush()
    module.atomic_move(nf.name, f.name)
    try:
        nf.close()
    except:
        pass
    res_args = dict(changed=changed, msg=message)
    if backup:
        res_args['backup_file'] = backup_file
    module.exit_json(**res_args)