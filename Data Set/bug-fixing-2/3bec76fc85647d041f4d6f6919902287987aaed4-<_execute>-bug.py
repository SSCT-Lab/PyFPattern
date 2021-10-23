

def _execute(self, variables=None):
    '\n        The primary workhorse of the executor system, this runs the task\n        on the specified host (which may be the delegated_to host) and handles\n        the retry/until and block rescue/always execution\n        '
    if (variables is None):
        variables = self._job_vars
    templar = Templar(loader=self._loader, shared_loader_obj=self._shared_loader_obj, variables=variables)
    context_validation_error = None
    try:
        self._play_context = self._play_context.set_task_and_variable_override(task=self._task, variables=variables, templar=templar)
        self._play_context.post_validate(templar=templar)
        if (not self._play_context.remote_addr):
            self._play_context.remote_addr = self._host.address
        self._play_context.update_vars(variables)
    except AnsibleError as e:
        context_validation_error = e
    try:
        if (not self._task.evaluate_conditional(templar, variables)):
            display.debug('when evaluation is False, skipping this task')
            return dict(changed=False, skipped=True, skip_reason='Conditional result was False', _ansible_no_log=self._play_context.no_log)
    except AnsibleError:
        if (self._loop_eval_error is not None):
            raise self._loop_eval_error
        if (self._task.action not in ['include', 'include_tasks', 'include_role']):
            raise
    if (self._loop_eval_error is not None):
        raise self._loop_eval_error
    if (context_validation_error is not None):
        raise context_validation_error
    if (self._task.action in ('include', 'include_tasks')):
        include_variables = self._task.args.copy()
        include_file = include_variables.pop('_raw_params', None)
        if (not include_file):
            return dict(failed=True, msg='No include file was specified to the include')
        include_file = templar.template(include_file)
        return dict(include=include_file, include_variables=include_variables)
    elif (self._task.action == 'include_role'):
        include_variables = self._task.args.copy()
        return dict(include_variables=include_variables)
    self._task.post_validate(templar=templar)
    if ('_variable_params' in self._task.args):
        variable_params = self._task.args.pop('_variable_params')
        if isinstance(variable_params, dict):
            display.deprecated('Using variables for task params is unsafe, especially if the variables come from an external source like facts', version='2.6')
            variable_params.update(self._task.args)
            self._task.args = variable_params
    if ((not self._connection) or (not getattr(self._connection, 'connected', False)) or (self._play_context.remote_addr != self._connection._play_context.remote_addr)):
        self._connection = self._get_connection(variables=variables, templar=templar)
    else:
        self._connection._play_context = self._play_context
    self._set_connection_options(variables, templar)
    self._set_shell_options(variables, templar)
    self._handler = self._get_action_handler(connection=self._connection, templar=templar)
    omit_token = variables.get('omit')
    if (omit_token is not None):
        self._task.args = remove_omit(self._task.args, omit_token)
    if self._task.until:
        retries = self._task.retries
        if (retries is None):
            retries = 3
        elif (retries <= 0):
            retries = 1
        else:
            retries += 1
    else:
        retries = 1
    delay = self._task.delay
    if (delay < 0):
        delay = 1
    vars_copy = variables.copy()
    display.debug('starting attempt loop')
    result = None
    for attempt in range(1, (retries + 1)):
        display.debug('running the handler')
        try:
            result = self._handler.run(task_vars=variables)
        except AnsibleActionSkip as e:
            return dict(skipped=True, msg=to_text(e))
        except AnsibleActionFail as e:
            return dict(failed=True, msg=to_text(e))
        except AnsibleConnectionFailure as e:
            return dict(unreachable=True, msg=to_text(e))
        display.debug('handler run complete')
        result['_ansible_no_log'] = self._play_context.no_log
        if self._task.register:
            vars_copy[self._task.register] = wrap_var(result)
        if (self._task.async_val > 0):
            if ((self._task.poll > 0) and (not result.get('skipped')) and (not result.get('failed'))):
                result = self._poll_async_result(result=result, templar=templar, task_vars=vars_copy)
            result['_ansible_no_log'] = self._play_context.no_log

        def _evaluate_changed_when_result(result):
            if ((self._task.changed_when is not None) and self._task.changed_when):
                cond = Conditional(loader=self._loader)
                cond.when = self._task.changed_when
                result['changed'] = cond.evaluate_conditional(templar, vars_copy)

        def _evaluate_failed_when_result(result):
            if self._task.failed_when:
                cond = Conditional(loader=self._loader)
                cond.when = self._task.failed_when
                failed_when_result = cond.evaluate_conditional(templar, vars_copy)
                result['failed_when_result'] = result['failed'] = failed_when_result
            else:
                failed_when_result = False
            return failed_when_result
        if ('ansible_facts' in result):
            vars_copy.update(namespace_facts(result['ansible_facts']))
            if C.INJECT_FACTS_AS_VARS:
                vars_copy.update(clean_facts(result['ansible_facts']))
        if ('failed' not in result):
            if (('rc' in result) and (result['rc'] not in [0, '0'])):
                result['failed'] = True
            else:
                result['failed'] = False
        if self._task.until:
            result['attempts'] = attempt
        if ('changed' not in result):
            result['changed'] = False
        if self._task.register:
            vars_copy[self._task.register] = wrap_var(result)
        if ('skipped' not in result):
            _evaluate_changed_when_result(result)
            _evaluate_failed_when_result(result)
        if (retries > 1):
            cond = Conditional(loader=self._loader)
            cond.when = self._task.until
            if cond.evaluate_conditional(templar, vars_copy):
                break
            elif (attempt < retries):
                result['_ansible_retry'] = True
                result['retries'] = retries
                display.debug(('Retrying task, attempt %d of %d' % (attempt, retries)))
                self._rslt_q.put(TaskResult(self._host.name, self._task._uuid, result, task_fields=self._task.dump_attrs()), block=False)
                time.sleep(delay)
    else:
        if (retries > 1):
            result['attempts'] = (retries - 1)
            result['failed'] = True
    if self._task.register:
        variables[self._task.register] = wrap_var(result)
    if ('ansible_facts' in result):
        variables.update(namespace_facts(result['ansible_facts']))
        if C.INJECT_FACTS_AS_VARS:
            variables.update(clean_facts(result['ansible_facts']))
    if (self._task.notify is not None):
        result['_ansible_notify'] = self._task.notify
    delegated_vars = variables.get('ansible_delegated_vars', dict()).get(self._task.delegate_to, dict()).copy()
    if (len(delegated_vars) > 0):
        result['_ansible_delegated_vars'] = {
            'ansible_delegated_host': self._task.delegate_to,
        }
        for k in ('ansible_host',):
            result['_ansible_delegated_vars'][k] = delegated_vars.get(k)
    display.debug('attempt loop complete, returning result')
    return result
