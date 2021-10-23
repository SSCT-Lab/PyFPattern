def run(self, tmp=None, task_vars=None):
    ' handler for file transfer operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    try:
        creates = self._task.args.get('creates')
        if creates:
            if self._remote_file_exists(creates):
                raise AnsibleActionSkip(('%s exists, matching creates option' % creates))
        removes = self._task.args.get('removes')
        if removes:
            if (not self._remote_file_exists(removes)):
                raise AnsibleActionSkip(('%s does not exist, matching removes option' % removes))
        chdir = self._task.args.get('chdir')
        if chdir:
            if ((self._connection._shell.SHELL_FAMILY == 'powershell') and (not self.windows_absolute_path_detection.match(chdir))):
                raise AnsibleActionFail(('chdir %s must be an absolute path for a Windows remote node' % chdir))
            if ((self._connection._shell.SHELL_FAMILY != 'powershell') and (not chdir.startswith('/'))):
                raise AnsibleActionFail(('chdir %s must be an absolute path for a Unix-aware remote node' % chdir))
        raw_params = to_native(self._task.args.get('_raw_params', ''), errors='surrogate_or_strict')
        parts = [to_text(s, errors='surrogate_or_strict') for s in shlex.split(raw_params.strip())]
        source = parts[0]
        executable = to_native(self._task.args.get('executable', ''), errors='surrogate_or_strict')
        try:
            source = self._loader.get_real_file(self._find_needle('files', source), decrypt=self._task.args.get('decrypt', True))
        except AnsibleError as e:
            raise AnsibleActionFail(to_native(e))
        result['changed'] = True
        if (not self._play_context.check_mode):
            tmp_src = self._connection._shell.join_path(self._connection._shell.tmpdir, os.path.basename(source))
            target_command = to_text(raw_params).strip().replace(parts[0], tmp_src)
            self._transfer_file(source, tmp_src)
            self._fixup_perms2((self._connection._shell.tmpdir, tmp_src), execute=True)
            env_dict = dict()
            env_string = self._compute_environment_string(env_dict)
            if executable:
                script_cmd = ' '.join([env_string, executable, target_command])
            else:
                script_cmd = ' '.join([env_string, target_command])
        if self._play_context.check_mode:
            raise _AnsibleActionDone()
        script_cmd = self._connection._shell.wrap_for_exec(script_cmd)
        exec_data = None
        if (self._connection._shell.SHELL_FAMILY == 'powershell'):
            pc = self._play_context
            exec_data = ps_manifest._create_powershell_wrapper(to_bytes(script_cmd), {
                
            }, env_dict, self._task.async_val, pc.become, pc.become_method, pc.become_user, pc.become_pass, pc.become_flags, substyle='script')
            script_cmd = self._connection._shell.build_module_command(env_string='', shebang='#!powershell', cmd='')
        result.update(self._low_level_execute_command(cmd=script_cmd, in_data=exec_data, sudoable=True, chdir=chdir))
        if (('rc' in result) and (result['rc'] != 0)):
            raise AnsibleActionFail('non-zero return code')
    except AnsibleAction as e:
        result.update(e.result)
    finally:
        self._remove_tmp_path(self._connection._shell.tmpdir)
    return result