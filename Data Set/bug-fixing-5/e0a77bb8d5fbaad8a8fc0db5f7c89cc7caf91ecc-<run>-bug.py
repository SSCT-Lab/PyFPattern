def run(self):
    '\n        Run the given playbook, based on the settings in the play which\n        may limit the runs to serialized groups, etc.\n        '
    result = 0
    entrylist = []
    entry = {
        
    }
    try:
        for playbook_path in self._playbooks:
            pb = Playbook.load(playbook_path, variable_manager=self._variable_manager, loader=self._loader)
            self._inventory.set_playbook_basedir(os.path.realpath(os.path.dirname(playbook_path)))
            if (self._tqm is None):
                entry = {
                    'playbook': playbook_path,
                }
                entry['plays'] = []
            else:
                self._tqm.load_callbacks()
                self._tqm.send_callback('v2_playbook_on_start', pb)
            i = 1
            plays = pb.get_plays()
            display.vv(('%d plays in %s' % (len(plays), to_text(playbook_path))))
            for play in plays:
                if (play._included_path is not None):
                    self._loader.set_basedir(play._included_path)
                else:
                    self._loader.set_basedir(pb._basedir)
                self._inventory.remove_restriction()
                if play.vars_prompt:
                    for var in play.vars_prompt:
                        vname = var['name']
                        prompt = var.get('prompt', vname)
                        default = var.get('default', None)
                        private = var.get('private', True)
                        confirm = var.get('confirm', False)
                        encrypt = var.get('encrypt', None)
                        salt_size = var.get('salt_size', None)
                        salt = var.get('salt', None)
                        if (vname not in self._variable_manager.extra_vars):
                            if self._tqm:
                                self._tqm.send_callback('v2_playbook_on_vars_prompt', vname, private, prompt, encrypt, confirm, salt_size, salt, default)
                                play.vars[vname] = display.do_var_prompt(vname, private, prompt, encrypt, confirm, salt_size, salt, default)
                            else:
                                play.vars[vname] = default
                all_vars = self._variable_manager.get_vars(loader=self._loader, play=play)
                templar = Templar(loader=self._loader, variables=all_vars)
                new_play = play.copy()
                new_play.post_validate(templar)
                if self._options.syntax:
                    continue
                if (self._tqm is None):
                    entry['plays'].append(new_play)
                else:
                    self._tqm._unreachable_hosts.update(self._unreachable_hosts)
                    previously_failed = len(self._tqm._failed_hosts)
                    previously_unreachable = len(self._tqm._unreachable_hosts)
                    break_play = False
                    for batch in self._get_serialized_batches(new_play):
                        if (len(batch) == 0):
                            self._tqm.send_callback('v2_playbook_on_play_start', new_play)
                            self._tqm.send_callback('v2_playbook_on_no_hosts_matched')
                            break
                        self._inventory.restrict_to_hosts(batch)
                        result = self._tqm.run(play=play)
                        if ((result & self._tqm.RUN_FAILED_BREAK_PLAY) != 0):
                            result = self._tqm.RUN_FAILED_HOSTS
                            break_play = True
                        failed_hosts_count = ((len(self._tqm._failed_hosts) + len(self._tqm._unreachable_hosts)) - (previously_failed + previously_unreachable))
                        if (len(batch) == failed_hosts_count):
                            break_play = True
                            break
                        previously_failed += (len(self._tqm._failed_hosts) - previously_failed)
                        previously_unreachable += (len(self._tqm._unreachable_hosts) - previously_unreachable)
                        self._unreachable_hosts.update(self._tqm._unreachable_hosts)
                    if break_play:
                        break
                i = (i + 1)
            if entry:
                entrylist.append(entry)
            if (self._tqm is not None):
                if C.RETRY_FILES_ENABLED:
                    retries = set(self._tqm._failed_hosts.keys())
                    retries.update(self._tqm._unreachable_hosts.keys())
                    retries = sorted(retries)
                    if (len(retries) > 0):
                        if C.RETRY_FILES_SAVE_PATH:
                            basedir = C.shell_expand(C.RETRY_FILES_SAVE_PATH)
                        elif playbook_path:
                            basedir = os.path.dirname(playbook_path)
                        else:
                            basedir = '~/'
                        (retry_name, _) = os.path.splitext(os.path.basename(playbook_path))
                        filename = os.path.join(basedir, ('%s.retry' % retry_name))
                        if self._generate_retry_inventory(filename, retries):
                            display.display(('\tto retry, use: --limit @%s\n' % filename))
                self._tqm.send_callback('v2_playbook_on_stats', self._tqm._stats)
            if (result != 0):
                break
        if entrylist:
            return entrylist
    finally:
        if (self._tqm is not None):
            self._tqm.cleanup()
        if self._loader:
            self._loader.cleanup_all_tmp_files()
    if self._options.syntax:
        display.display('No issues encountered')
        return result
    return result