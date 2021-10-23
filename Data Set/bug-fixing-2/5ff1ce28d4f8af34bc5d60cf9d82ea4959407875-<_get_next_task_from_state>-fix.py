

def _get_next_task_from_state(self, state, host, peek, in_child=False):
    task = None
    while True:
        try:
            block = state._blocks[state.cur_block]
        except IndexError:
            state.run_state = self.ITERATING_COMPLETE
            return (state, None)
        if (state.run_state == self.ITERATING_SETUP):
            if (not state.pending_setup):
                state.pending_setup = True
                gathering = C.DEFAULT_GATHERING
                implied = ((self._play.gather_facts is None) or boolean(self._play.gather_facts, strict=False))
                if (((gathering == 'implicit') and implied) or ((gathering == 'explicit') and boolean(self._play.gather_facts, strict=False)) or ((gathering == 'smart') and implied and (not self._variable_manager._fact_cache.get(host.name, {
                    
                }).get('_ansible_facts_gathered', False)))):
                    setup_block = self._blocks[0]
                    if (setup_block.has_tasks() and (len(setup_block.block) > 0)):
                        task = setup_block.block[0]
            else:
                state.pending_setup = False
                state.run_state = self.ITERATING_TASKS
                if (not state.did_start_at_task):
                    state.cur_block += 1
                    state.cur_regular_task = 0
                    state.cur_rescue_task = 0
                    state.cur_always_task = 0
                    state.tasks_child_state = None
                    state.rescue_child_state = None
                    state.always_child_state = None
        elif (state.run_state == self.ITERATING_TASKS):
            if state.pending_setup:
                state.pending_setup = False
            if state.tasks_child_state:
                (state.tasks_child_state, task) = self._get_next_task_from_state(state.tasks_child_state, host=host, peek=peek, in_child=True)
                if self._check_failed_state(state.tasks_child_state):
                    state.tasks_child_state = None
                    self._set_failed_state(state)
                elif ((task is None) or (state.tasks_child_state.run_state == self.ITERATING_COMPLETE)):
                    state.tasks_child_state = None
                    continue
            elif self._check_failed_state(state):
                state.run_state = self.ITERATING_RESCUE
            elif (state.cur_regular_task >= len(block.block)):
                state.run_state = self.ITERATING_ALWAYS
            else:
                task = block.block[state.cur_regular_task]
                if isinstance(task, Block):
                    state.tasks_child_state = HostState(blocks=[task])
                    state.tasks_child_state.run_state = self.ITERATING_TASKS
                    task = None
                state.cur_regular_task += 1
        elif (state.run_state == self.ITERATING_RESCUE):
            if (host.name in self._play._removed_hosts):
                self._play._removed_hosts.remove(host.name)
            if state.rescue_child_state:
                (state.rescue_child_state, task) = self._get_next_task_from_state(state.rescue_child_state, host=host, peek=peek, in_child=True)
                if self._check_failed_state(state.rescue_child_state):
                    state.rescue_child_state = None
                    self._set_failed_state(state)
                elif ((task is None) or (state.rescue_child_state.run_state == self.ITERATING_COMPLETE)):
                    state.rescue_child_state = None
                    continue
            elif ((state.fail_state & self.FAILED_RESCUE) == self.FAILED_RESCUE):
                state.run_state = self.ITERATING_ALWAYS
            elif (state.cur_rescue_task >= len(block.rescue)):
                if (len(block.rescue) > 0):
                    state.fail_state = self.FAILED_NONE
                state.run_state = self.ITERATING_ALWAYS
                state.did_rescue = True
            else:
                task = block.rescue[state.cur_rescue_task]
                if isinstance(task, Block):
                    state.rescue_child_state = HostState(blocks=[task])
                    state.rescue_child_state.run_state = self.ITERATING_TASKS
                    task = None
                state.cur_rescue_task += 1
        elif (state.run_state == self.ITERATING_ALWAYS):
            if state.always_child_state:
                (state.always_child_state, task) = self._get_next_task_from_state(state.always_child_state, host=host, peek=peek, in_child=True)
                if self._check_failed_state(state.always_child_state):
                    state.always_child_state = None
                    self._set_failed_state(state)
                elif ((task is None) or (state.always_child_state.run_state == self.ITERATING_COMPLETE)):
                    state.always_child_state = None
                    continue
            elif (state.cur_always_task >= len(block.always)):
                if (state.fail_state != self.FAILED_NONE):
                    state.run_state = self.ITERATING_COMPLETE
                else:
                    state.cur_block += 1
                    state.cur_regular_task = 0
                    state.cur_rescue_task = 0
                    state.cur_always_task = 0
                    state.run_state = self.ITERATING_TASKS
                    state.tasks_child_state = None
                    state.rescue_child_state = None
                    state.always_child_state = None
                    state.did_rescue = False
                    if (block._eor and (host.name in block._role._had_task_run) and (not in_child) and (not peek)):
                        block._role._completed[host.name] = True
            else:
                task = block.always[state.cur_always_task]
                if isinstance(task, Block):
                    state.always_child_state = HostState(blocks=[task])
                    state.always_child_state.run_state = self.ITERATING_TASKS
                    task = None
                state.cur_always_task += 1
        elif (state.run_state == self.ITERATING_COMPLETE):
            return (state, None)
        if task:
            break
    return (state, task)
