def test_log_exception(self):

    def call(self):
        with self.log():
            raise TypeError
    setattr(self.mediator, 'call', types.MethodType(call, self.mediator))
    with patch.object(self.logger, 'info') as mock:
        try:
            self.mediator.call()
        except Exception:
            pass
    call = mock.mock_calls[(- 1)][(- 1)]
    assert (call['extra']['at'] == 'exception')
    assert ('elapsed' in call['extra'])