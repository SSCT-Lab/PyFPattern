

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
        success_cmd = shlex_quote(('echo %s; %s' % (success_key, cmd)))
        if executable:
            command = ('%s -c %s' % (executable, success_cmd))
        else:
            command = success_cmd
        exe = (self.become_exe or getattr(self, ('%s_exe' % self.become_method), self.become_method))
        flags = (self.become_flags or getattr(self, ('%s_flags' % self.become_method), ''))
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
            becomecmd = ('%s %s %s -c %s' % (exe, flags, self.become_user, shlex_quote(command)))
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
            display.warning("The Windows 'runas' become method is experimental, and may change significantly in future Ansible releases.")
            if (not self.become_user):
                raise AnsibleError("The 'runas' become method requires a username (specify with the '--become-user' CLI arg, the 'become_user' keyword, or the 'ansible_become_user' variable)")
            if (not self.become_pass):
                raise AnsibleError("The 'runas' become method requires a password (specify with the '-K' CLI arg or the 'ansible_become_password' variable)")
            becomecmd = cmd
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
                becomecmd = ('%s -p %s -u %s %s' % (exe, shlex_quote(prompt), self.become_user, command))
            else:
                becomecmd = ('%s -u %s %s' % (exe, self.become_user, command))
        elif (self.become_method == 'pmrun'):
            exe = (self.become_exe or 'pmrun')
            prompt = 'Enter UPM user password:'
            becomecmd = ('%s %s %s' % (exe, flags, shlex_quote(command)))
        else:
            raise AnsibleError(('Privilege escalation method not found: %s' % self.become_method))
        if self.become_pass:
            self.prompt = prompt
        self.success_key = success_key
        return becomecmd
    return cmd
