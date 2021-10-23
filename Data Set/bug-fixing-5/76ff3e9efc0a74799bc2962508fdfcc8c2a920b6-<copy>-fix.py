def copy(self, exclude_parent=False, exclude_tasks=False):

    def _dupe_task_list(task_list, new_block):
        new_task_list = []
        for task in task_list:
            new_task = task.copy(exclude_parent=True)
            if task._parent:
                new_task._parent = task._parent.copy(exclude_tasks=True)
                cur_obj = new_task
                while cur_obj._parent:
                    if cur_obj._parent:
                        prev_obj = cur_obj
                    cur_obj = cur_obj._parent
                if (cur_obj != new_block):
                    cur_obj._parent = new_block
                else:
                    prev_obj._parent = new_block
            else:
                new_task._parent = new_block
            new_task_list.append(new_task)
        return new_task_list
    new_me = super(Block, self).copy()
    new_me._play = self._play
    new_me._use_handlers = self._use_handlers
    new_me._eor = self._eor
    if (self._dep_chain is not None):
        new_me._dep_chain = self._dep_chain[:]
    new_me._parent = None
    if (self._parent and (not exclude_parent)):
        new_me._parent = self._parent.copy(exclude_tasks=exclude_tasks)
    if (not exclude_tasks):
        new_me.block = _dupe_task_list((self.block or []), new_me)
        new_me.rescue = _dupe_task_list((self.rescue or []), new_me)
        new_me.always = _dupe_task_list((self.always or []), new_me)
    new_me._role = None
    if self._role:
        new_me._role = self._role
    new_me.validate()
    return new_me