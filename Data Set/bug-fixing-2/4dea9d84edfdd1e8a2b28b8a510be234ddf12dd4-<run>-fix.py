

def run(self):
    '\n        The main executor entrypoint, where we determine if the specified\n        task requires looping and either runs the task with self._run_loop()\n        or self._execute(). After that, the returned results are parsed and\n        returned as a dict.\n        '
    display.debug(('in run() - task %s' % self._task._uuid))
    try:
        try:
            items = self._get_loop_items()
        except AnsibleUndefinedVariable as e:
            items = None
            self._loop_eval_error = e
        if (items is not None):
            if (len(items) > 0):
                item_results = self._run_loop(items)
                res = dict(results=item_results)
                for item in item_results:
                    if (('changed' in item) and item['changed'] and (not res.get('changed'))):
                        res['changed'] = True
                    if (('failed' in item) and item['failed']):
                        item_ignore = item.pop('_ansible_ignore_errors')
                        if (not res.get('failed')):
                            res['failed'] = True
                            res['msg'] = 'One or more items failed'
                            self._task.ignore_errors = item_ignore
                        elif (self._task.ignore_errors and (not item_ignore)):
                            self._task.ignore_errors = item_ignore
                    for array in ['warnings', 'deprecations']:
                        if ((array in item) and item[array]):
                            if (array not in res):
                                res[array] = []
                            if (not isinstance(item[array], list)):
                                item[array] = [item[array]]
                            res[array] = (res[array] + item[array])
                            del item[array]
                if (not res.get('Failed', False)):
                    res['msg'] = 'All items completed'
            else:
                res = dict(changed=False, skipped=True, skipped_reason='No items in the list', results=[])
        else:
            display.debug('calling self._execute()')
            res = self._execute()
            display.debug('_execute() done')
        if ('changed' not in res):
            res['changed'] = False

        def _clean_res(res, errors='surrogate_or_strict'):
            if isinstance(res, UnsafeProxy):
                return res._obj
            elif isinstance(res, binary_type):
                return to_text(res, errors=errors)
            elif isinstance(res, dict):
                for k in res:
                    try:
                        res[k] = _clean_res(res[k], errors=errors)
                    except UnicodeError:
                        if (k == 'diff'):
                            display.warning('We were unable to decode all characters in the module return data. Replaced some in an effort to return as much as possible')
                            res[k] = _clean_res(res[k], errors='surrogate_then_replace')
                        else:
                            raise
            elif isinstance(res, list):
                for (idx, item) in enumerate(res):
                    res[idx] = _clean_res(item, errors=errors)
            return res
        display.debug('dumping result to json')
        res = _clean_res(res)
        display.debug('done dumping result, returning')
        return res
    except AnsibleError as e:
        return dict(failed=True, msg=wrap_var(to_text(e, nonstring='simplerepr')), _ansible_no_log=self._play_context.no_log)
    except Exception as e:
        return dict(failed=True, msg='Unexpected failure during module execution.', exception=to_text(traceback.format_exc()), stdout='', _ansible_no_log=self._play_context.no_log)
    finally:
        try:
            self._connection.close()
        except AttributeError:
            pass
        except Exception as e:
            display.debug(('error closing connection: %s' % to_text(e)))
