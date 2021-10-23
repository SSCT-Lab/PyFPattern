def _run_loop(self, items):
    "\n        Runs the task with the loop items specified and collates the result\n        into an array named 'results' which is inserted into the final result\n        along with the item for which the loop ran.\n        "
    results = []
    task_vars = self._job_vars
    loop_var = 'item'
    index_var = None
    label = None
    loop_pause = 0
    templar = Templar(loader=self._loader, shared_loader_obj=self._shared_loader_obj, variables=self._job_vars)
    if self._task.loop_control:
        loop_var = templar.template(self._task.loop_control.loop_var)
        index_var = templar.template(self._task.loop_control.index_var)
        loop_pause = templar.template(self._task.loop_control.pause)
        label = (self._task.loop_control.label or (('{{' + loop_var) + '}}'))
    if (loop_var in task_vars):
        display.warning(("The loop variable '%s' is already in use. You should set the `loop_var` value in the `loop_control` option for the task to something else to avoid variable collisions and unexpected behavior." % loop_var))
    ran_once = False
    if self._task.loop_with:
        items = self._squash_items(items, loop_var, task_vars)
    for (item_index, item) in enumerate(items):
        task_vars[loop_var] = item
        if index_var:
            task_vars[index_var] = item_index
        if (loop_pause and ran_once):
            try:
                time.sleep(float(loop_pause))
            except ValueError as e:
                raise AnsibleError(('Invalid pause value: %s, produced error: %s' % (loop_pause, to_native(e))))
        else:
            ran_once = True
        try:
            tmp_task = self._task.copy(exclude_parent=True, exclude_tasks=True)
            tmp_task._parent = self._task._parent
            tmp_play_context = self._play_context.copy()
        except AnsibleParserError as e:
            results.append(dict(failed=True, msg=to_text(e)))
            continue
        (self._task, tmp_task) = (tmp_task, self._task)
        (self._play_context, tmp_play_context) = (tmp_play_context, self._play_context)
        res = self._execute(variables=task_vars)
        task_fields = self._task.dump_attrs()
        (self._task, tmp_task) = (tmp_task, self._task)
        (self._play_context, tmp_play_context) = (tmp_play_context, self._play_context)
        res[loop_var] = item
        if index_var:
            res[index_var] = item_index
        res['_ansible_item_result'] = True
        res['_ansible_ignore_errors'] = task_fields.get('ignore_errors')
        if (label is not None):
            res['_ansible_item_label'] = templar.template(label, cache=False)
        self._rslt_q.put(TaskResult(self._host.name, self._task._uuid, res, task_fields=task_fields), block=False)
        results.append(res)
        del task_vars[loop_var]
    return results