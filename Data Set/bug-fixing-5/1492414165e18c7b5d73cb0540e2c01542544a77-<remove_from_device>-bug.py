def remove_from_device(self):
    result = self.client.api.tm.cm.remove_from_trust.exec_cmd('run', deviceName=self.want.peer_hostname, name=self.want.peer_hostname)