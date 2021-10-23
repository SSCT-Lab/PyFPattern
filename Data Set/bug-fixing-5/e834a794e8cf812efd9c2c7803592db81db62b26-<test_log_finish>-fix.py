def test_log_finish(self):
    with patch.object(self.logger, 'info') as mock:
        self.mediator.call()
    call = mock.mock_calls[(- 1)][(- 1)]
    assert (call['extra']['at'] == 'finish')
    assert ('elapsed' in call['extra'])