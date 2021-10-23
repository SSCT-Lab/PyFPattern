def main():
    module = AnsibleModule(argument_spec=dict(name=dict(type='str'), user=dict(type='str'), job=dict(type='str', aliases=['value']), cron_file=dict(type='str'), state=dict(type='str', default='present', choices=['present', 'absent']), backup=dict(type='bool', default=False), minute=dict(type='str', default='*'), hour=dict(type='str', default='*'), day=dict(type='str', default='*', aliases=['dom']), month=dict(type='str', default='*'), weekday=dict(type='str', default='*', aliases=['dow']), reboot=dict(type='bool', default=False), special_time=dict(type='str', choices=['reboot', 'yearly', 'annually', 'monthly', 'weekly', 'daily', 'hourly']), disabled=dict(type='bool', default=False), env=dict(type='bool'), insertafter=dict(type='str'), insertbefore=dict(type='str')), supports_check_mode=True, mutually_exclusive=[['reboot', 'special_time'], ['insertafter', 'insertbefore']])
    name = module.params['name']
    user = module.params['user']
    job = module.params['job']
    cron_file = module.params['cron_file']
    state = module.params['state']
    backup = module.params['backup']
    minute = module.params['minute']
    hour = module.params['hour']
    day = module.params['day']
    month = module.params['month']
    weekday = module.params['weekday']
    reboot = module.params['reboot']
    special_time = module.params['special_time']
    disabled = module.params['disabled']
    env = module.params['env']
    insertafter = module.params['insertafter']
    insertbefore = module.params['insertbefore']
    do_install = (state == 'present')
    changed = False
    res_args = dict()
    warnings = list()
    if cron_file:
        cron_file_basename = os.path.basename(cron_file)
        if (not re.search('^[A-Z0-9_-]+$', cron_file_basename, re.I)):
            warnings.append((('Filename portion of cron_file ("%s") should consist' % cron_file_basename) + ' solely of upper- and lower-case letters, digits, underscores, and hyphens'))
    os.umask(int('022', 8))
    crontab = CronTab(module, user, cron_file)
    module.debug(('cron instantiated - name: "%s"' % name))
    if (not name):
        module.deprecate(msg="The 'name' parameter will be required in future releases.", version='2.12')
    if reboot:
        module.deprecate(msg="The 'reboot' parameter will be removed in future releases. Use 'special_time' option instead.", version='2.12')
    if module._diff:
        diff = dict()
        diff['before'] = crontab.existing
        if crontab.cron_file:
            diff['before_header'] = crontab.cron_file
        elif crontab.user:
            diff['before_header'] = ('crontab for user "%s"' % crontab.user)
        else:
            diff['before_header'] = 'crontab'
    if ((special_time or reboot) and (True in [(x != '*') for x in [minute, hour, day, month, weekday]])):
        module.fail_json(msg='You must specify time and date fields or special time.')
    if ((special_time or reboot) and (get_platform() == 'SunOS')):
        module.fail_json(msg='Solaris does not support special_time=... or @reboot')
    if (cron_file and do_install):
        if (not user):
            module.fail_json(msg='To use cron_file=... parameter you must specify user=... as well')
    if ((job is None) and do_install):
        module.fail_json(msg="You must specify 'job' to install a new cron job or variable")
    if ((insertafter or insertbefore) and (not env) and do_install):
        module.fail_json(msg='Insertafter and insertbefore parameters are valid only with env=yes')
    if reboot:
        special_time = 'reboot'
    if (backup and (not module.check_mode)):
        (backuph, backup_file) = tempfile.mkstemp(prefix='crontab')
        crontab.write(backup_file)
    if (crontab.cron_file and (not name) and (not do_install)):
        if module._diff:
            diff['after'] = ''
            diff['after_header'] = '/dev/null'
        else:
            diff = dict()
        if module.check_mode:
            changed = os.path.isfile(crontab.cron_file)
        else:
            changed = crontab.remove_job_file()
        module.exit_json(changed=changed, cron_file=cron_file, state=state, diff=diff)
    if env:
        if (' ' in name):
            module.fail_json(msg='Invalid name for environment variable')
        decl = ('%s="%s"' % (name, job))
        old_decl = crontab.find_env(name)
        if do_install:
            if (len(old_decl) == 0):
                crontab.add_env(decl, insertafter, insertbefore)
                changed = True
            if ((len(old_decl) > 0) and (old_decl[1] != decl)):
                crontab.update_env(name, decl)
                changed = True
        elif (len(old_decl) > 0):
            crontab.remove_env(name)
            changed = True
    elif do_install:
        for char in ['\r', '\n']:
            if (char in job.strip('\r\n')):
                warnings.append('Job should not contain line breaks')
                break
        job = crontab.get_cron_job(minute, hour, day, month, weekday, job, special_time, disabled)
        old_job = crontab.find_job(name, job)
        if (len(old_job) == 0):
            crontab.add_job(name, job)
            changed = True
        if ((len(old_job) > 0) and (old_job[1] != job)):
            crontab.update_job(name, job)
            changed = True
        if (len(old_job) > 2):
            crontab.update_job(name, job)
            changed = True
    else:
        old_job = crontab.find_job(name)
        if (len(old_job) > 0):
            crontab.remove_job(name)
            changed = True
    if ((not changed) and (crontab.existing != '')):
        if (not (crontab.existing.endswith('\r') or crontab.existing.endswith('\n'))):
            changed = True
    res_args = dict(jobs=crontab.get_jobnames(), envs=crontab.get_envnames(), warnings=warnings, changed=changed)
    if changed:
        if (not module.check_mode):
            crontab.write()
        if module._diff:
            diff['after'] = crontab.render()
            if crontab.cron_file:
                diff['after_header'] = crontab.cron_file
            elif crontab.user:
                diff['after_header'] = ('crontab for user "%s"' % crontab.user)
            else:
                diff['after_header'] = 'crontab'
            res_args['diff'] = diff
    if (backup and (not module.check_mode)):
        if changed:
            res_args['backup_file'] = backup_file
        else:
            os.unlink(backup_file)
    if cron_file:
        res_args['cron_file'] = cron_file
    module.exit_json(**res_args)
    module.exit_json(msg='Unable to execute cron task.')