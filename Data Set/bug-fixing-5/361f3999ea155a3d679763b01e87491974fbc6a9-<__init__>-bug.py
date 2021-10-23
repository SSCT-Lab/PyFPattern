def __init__(self):
    if (not HAS_PYEZ):
        raise NetworkError(msg='junos-eznc >= 1.2.2 is required but does not appear to be installed.  It can be installed using `pip install junos-eznc`')
    if (not HAS_JXMLEASE):
        raise NetworkError(msg='jxmlease is required but does not appear to be installed.  It can be installed using `pip install jxmlease`')
    self.device = None
    self.config = None
    self._locked = False
    self._connected = False
    self.default_output = 'xml'