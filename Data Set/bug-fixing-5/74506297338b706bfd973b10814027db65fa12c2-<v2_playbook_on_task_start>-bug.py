def v2_playbook_on_task_start(self, task, is_conditional):
    args = ''
    if ((not task.no_log) and C.DISPLAY_ARGS_TO_STDOUT):
        args = ', '.join((('%s=%s' % a) for a in task.args.items()))
        args = (' %s' % args)
    self._display.banner(('TASK [%s%s]' % (task.get_name().strip(), args)))
    if (self._display.verbosity >= 2):
        path = task.get_path()
        if path:
            self._display.display(('task path: %s' % path), color=C.COLOR_DEBUG)