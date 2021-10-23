def make_become_cmd(self, cmd, executable=None):
    ' helper function to create privilege escalation commands '
    prompt = None
    success_key = None
    self.prompt = None
    if self.become:
        if (not executable):
            executable = self.executable
        becomecmd = None
        randbits = ''.join((random.choice(string.ascii_lowercase) for x in range(32)))
        success_key = ('BECOME-SUCCESS-%s' % randbits)
        success_cmd = pipes.quote(('echo %s; %s' % (success_key, cmd)))
        if executable:
            command = ('%s -c %s' % (executable, success_cmd))
        else:
            command = success_cmd
        exe = (self.become_exe or getattr(self, ('%s_exe' % self.become_method), None) or C.DEFAULT_BECOME_EXE or getattr(C, ('DEFAULT_%s_EXE' % self.become_method.upper()), None) or self.become_method)
        flags = (self.become_flags or getattr(self, ('%s_flags' % self.become_method), None) or C.DEFAULT_BECOME_FLAGS or getattr(C, ('DEFAULT_%s_FLAGS' % self.become_method.upper()), None) or '')
        if (self.become_method == 'sudo'):
            if self.become_pass:
                prompt = ('[sudo via ansible, key=%s] password: ' % randbits)
                becomecmd = ('%s %s -p "%s" -u %s %s' % (exe, flags.replace('-n', ''), prompt, self.become_user, command))
            else:
                becomecmd = ('%s %s -u %s %s' % (exe, flags, self.become_user, command))
        elif (self.become_method == 'su'):

            def detect_su_prompt(b_data):
                b_password_string = b'|'.join([(b"(\\w+'s )?" + x) for x in b_SU_PROMPT_LOCALIZATIONS])
                b_password_string = (b_password_string + to_bytes(' ?(:|：) ?'))
                b_SU_PROMPT_LOCALIZATIONS_RE = re.compile(b_password_string, flags=re.IGNORECASE)
                return bool(b_SU_PROMPT_LOCALIZATIONS_RE.match(b_data))
            prompt = detect_su_prompt
            becomecmd = ('%s %s %s -c %s' % (exe, flags, self.become_user, pipes.quote(command)))
        elif (self.become_method == 'pbrun'):
            prompt = 'Password:'
            becomecmd = ('%s %s -u %s %s' % (exe, flags, self.become_user, success_cmd))
        elif (self.become_method == 'ksu'):

            def detect_ksu_prompt(b_data):
                return re.match(b'Kerberos password for .*@.*:', b_data)
            prompt = detect_ksu_prompt
            becomecmd = ('%s %s %s -e %s' % (exe, self.become_user, flags, command))
        elif (self.become_method == 'pfexec'):
            becomecmd = ('%s %s "%s"' % (exe, flags, success_cmd))
        elif (self.become_method == 'runas'):
            raise AnsibleError("'runas' is not yet implemented")
            becomecmd = ('%s %s /user:%s "%s"' % (exe, flags, self.become_user, success_cmd))
        elif (self.become_method == 'doas'):
            prompt = ('doas (%s@' % self.remote_user)
            exe = (self.become_exe or 'doas')
            if (not self.become_pass):
                flags += ' -n '
            if self.become_user:
                flags += (' -u %s ' % self.become_user)
            becomecmd = ('%s %s echo %s && %s %s env ANSIBLE=true %s' % (exe, flags, success_key, exe, flags, cmd))
        elif (self.become_method == 'dzdo'):
            exe = (self.become_exe or 'dzdo')
            if self.become_pass:
                prompt = ('[dzdo via ansible, key=%s] password: ' % randbits)
                becomecmd = ('%s -p %s -u %s %s' % (exe, pipes.quote(prompt), self.become_user, command))
            else:
                becomecmd = ('%s -u %s %s' % (exe, self.become_user, command))
        else:
            raise AnsibleError(('Privilege escalation method not found: %s' % self.become_method))
        if self.become_pass:
            self.prompt = prompt
        self.success_key = success_key
        return becomecmd
    return cmd