

def _poll_async_result(self, result, templar, task_vars=None):
    '\n        Polls for the specified JID to be complete\n        '
    if (task_vars is None):
        task_vars = self._job_vars
    async_jid = result.get('ansible_job_id')
    if (async_jid is None):
        return dict(failed=True, msg='No job id was returned by the async task')
    async_task = Task().load(dict(action=('async_status jid=%s' % async_jid), environment=self._task.environment))
    normal_handler = self._shared_loader_obj.action_loader.get('normal', task=async_task, connection=self._connection, play_context=self._play_context, loader=self._loader, templar=templar, shared_loader_obj=self._shared_loader_obj)
    time_left = self._task.async_val
    while (time_left > 0):
        time.sleep(self._task.poll)
        try:
            async_result = normal_handler.run(task_vars=task_vars)
            if ((int(async_result.get('finished', 0)) == 1) or (('failed' in async_result) and async_result.get('_ansible_parsed', False)) or ('skipped' in async_result)):
                break
        except Exception as e:
            display.vvvv(('Exception during async poll, retrying... (%s)' % to_text(e)))
            display.debug(('Async poll exception was:\n%s' % to_text(traceback.format_exc())))
            try:
                normal_handler._connection._reset()
            except AttributeError:
                pass
            time_left -= self._task.poll
            if (time_left <= 0):
                raise
        else:
            time_left -= self._task.poll
    if (int(async_result.get('finished', 0)) != 1):
        if async_result.get('_ansible_parsed'):
            return dict(failed=True, msg='async task did not complete within the requested time')
        else:
            return dict(failed=True, msg='async task produced unparseable results', async_result=async_result)
    else:
        return async_result
