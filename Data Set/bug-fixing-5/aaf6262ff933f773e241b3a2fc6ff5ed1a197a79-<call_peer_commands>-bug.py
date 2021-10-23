def call_peer_commands(self):
    result = {
        
    }
    result['msg'] = ''
    result['changed'] = False
    for node in self.nodes:
        peercmd = [self.glustercmd, 'peer', self.action, node]
        if self.force:
            peercmd.append(self.force)
        (rc, out, err) = self.module.run_command(peercmd, environ_update=self.lang)
        if rc:
            result['rc'] = rc
            result['msg'] = err
            self.module.fail_json(**result)
        elif (('already in peer' in out) or ('localhost not needed' in out)):
            result['changed'] |= False
        else:
            result['changed'] = True
    self.module.exit_json(**result)