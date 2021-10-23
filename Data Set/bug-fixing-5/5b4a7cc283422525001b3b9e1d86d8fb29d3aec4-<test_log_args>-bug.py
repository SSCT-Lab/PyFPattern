@pytest.mark.parametrize('stdin', ({
    
},), indirect=['stdin'])
def test_log_args(self, am, mocker):
    journal_send = mocker.patch('systemd.journal.send')
    am.log('unittest log_args', log_args=dict(TEST='log unittest'))
    assert (journal_send.called == 1)
    assert journal_send.call_args[0][0].endswith('unittest log_args'), 'Message was not sent to log'
    assert ('MODULE' in journal_send.call_args[1])
    assert ('basic.py' in journal_send.call_args[1]['MODULE'])
    assert ('TEST' in journal_send.call_args[1])
    assert ('log unittest' in journal_send.call_args[1]['TEST'])