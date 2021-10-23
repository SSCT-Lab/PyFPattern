

def main():
    module = AnsibleModule(argument_spec=dict(name=dict(required=False), user=dict(required=False), job=dict(required=False, aliases=['value']), cron_file=dict(required=False), state=dict(default='present', choices=['present', 'absent']), backup=dict(default=False, type='bool'), minute=dict(default='*'), hour=dict(default='*'), day=dict(aliases=['dom'], default='*'), month=dict(default='*'), weekday=dict(aliases=['dow'], default='*'), reboot=dict(required=False, default=False, type='bool'), special_time=dict(required=False, default=None, choices=['reboot', 'yearly', 'annually', 'monthly', 'weekly', 'daily', 'hourly'], type='str'), disabled=dict(default=False, type='bool'), env=dict(required=False, type='bool'), insertafter=dict(required=False), insertbefore=dict(required=False)), supports_check_mode=True, mutually_exclusive=[['reboot', 'special_time'], ['insertafter', 'insertbefore']])
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
    os.umask(int('022', 8))
    crontab = CronTab(module, user, cron_file)
    module.debug(('cron instantiated - name: "%s"' % name))
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
    if ((not changed) and (not (crontab.existing == ''))):
        if (not (crontab.existing.endswith('\r') or crontab.existing.endswith('\n'))):
            changed = True
    res_args = dict(jobs=crontab.get_jobnames(), envs=crontab.get_envnames(), changed=changed)
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
    if backup:
        if changed:
            res_args['backup_file'] = backup_file
        elif (not module.check_mode):
            os.unlink(backup_file)
    if cron_file:
        res_args['cron_file'] = cron_file
    module.exit_json(**res_args)
    module.exit_json(msg='Unable to execute cron task.')
