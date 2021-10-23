

def main():
    gunicorn_options = {
        'config': '-c',
        'chdir': '--chdir',
        'worker': '-k',
        'user': '-u',
    }
    tmp_error_log = '/tmp/gunicorn.temp.error.log'
    tmp_pid_file = '/tmp/gunicorn.temp.pid'
    remove_tmp_file(tmp_pid_file)
    remove_tmp_file(tmp_error_log)
    module = AnsibleModule(argument_spec=dict(app=dict(required=True, type='str', aliases=['name']), venv=dict(required=False, type='path', default=None, aliases=['virtualenv']), config=dict(required=False, default=None, type='path', aliases=['conf']), chdir=dict(required=False, type='path', default=None), pid=dict(required=False, type='path', default=None), user=dict(required=False, type='str'), worker=dict(required=False, type='str', choices=['sync', 'eventlet', 'gevent', 'tornado ', 'gthread', 'gaiohttp'])))
    params = module.params
    app = params['app']
    venv = params['venv']
    pid = params['pid']
    if venv:
        gunicorn_command = '/'.join((venv, 'bin', 'gunicorn'))
    else:
        gunicorn_command = 'gunicorn'
    options = ['-D']
    for option in gunicorn_options:
        param = params[option]
        if param:
            options.append(gunicorn_options[option])
            options.append(param)
    error_log = search_existing_config(params['config'], 'errorlog')
    if (not error_log):
        options.append('--error-logfile')
        options.append(tmp_error_log)
    pid_file = search_existing_config(params['config'], 'pid')
    if ((not params['pid']) and (not pid_file)):
        pid = tmp_pid_file
    if (not pid_file):
        options.append('--pid')
        options.append(pid)
    args = (([gunicorn_command] + options) + [app])
    (rc, out, err) = module.run_command(args, use_unsafe_shell=False, encoding=None)
    if (not err):
        time.sleep(0.5)
        if os.path.isfile(pid):
            with open(pid, 'r') as f:
                result = f.readline().strip()
            if (not params['pid']):
                os.remove(pid)
            module.exit_json(changed=True, pid=result, debug=' '.join(args))
        else:
            if error_log:
                error = 'Please check your {0}'.format(error_log.strip())
            elif os.path.isfile(tmp_error_log):
                with open(tmp_error_log, 'r') as f:
                    error = f.read()
                os.remove(tmp_error_log)
            else:
                error = 'Log not found'
            module.fail_json(msg='Failed to start gunicorn. {0}'.format(error), error=err)
    else:
        module.fail_json(msg='Failed to start gunicorn {0}'.format(err), error=err)
