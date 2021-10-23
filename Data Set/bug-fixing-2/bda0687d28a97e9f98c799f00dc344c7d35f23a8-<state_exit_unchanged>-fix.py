

def state_exit_unchanged(self):
    'Exit with status message'
    if (not self.host_update):
        result = 'Host already disconnected'
    elif (self.reconnect_disconnected and (self.host_update.runtime.connectionState == 'disconnected')):
        self.state_reconnect_host()
    elif self.folder_name:
        result = ("Host already connected to vCenter '%s' in folder '%s'" % (self.vcenter, self.folder_name))
    elif self.cluster_name:
        result = ("Host already connected to vCenter '%s' in cluster '%s'" % (self.vcenter, self.cluster_name))
    self.module.exit_json(changed=False, result=str(result))
