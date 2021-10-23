def _get_qos(self):
    qos = None
    if ((self.param('qos') == '') or (self.param('pass_through') == 'enabled')):
        qos = otypes.Qos()
    elif self.param('qos'):
        qos = otypes.Qos(id=self._get_qos_id())
    return qos