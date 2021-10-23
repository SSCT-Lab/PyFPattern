def test_log_finish(self):
    with patch.object(self.logger, 'info') as mock:
        self.mediator.call()
    mock.assert_any_call(None, extra={
        'at': 'finish',
        'elapsed': 0,
    })