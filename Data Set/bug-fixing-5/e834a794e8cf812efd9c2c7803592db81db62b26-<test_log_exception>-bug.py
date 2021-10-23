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
    mock.assert_called_with(None, extra={
        'at': 'exception',
        'elapsed': 0,
    })