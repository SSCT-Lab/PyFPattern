def _get_qos(self):
    qos = None
    if self.param('qos'):
        qos = otypes.Qos(id=self._get_qos_id())
    elif ((self.param('qos') == '') or (self.param('pass_through') == 'enabled')):
        qos = otypes.Qos()
    return qos