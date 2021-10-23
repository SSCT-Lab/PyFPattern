@pytest.mark.skip(reason='test broken, fails when run in isolation')
def test_update_lambda_if_only_one_config_item_changed(monkeypatch):
    fake_lambda_connection = MagicMock()
    fake_lambda_connection.get_function.configure_mock(return_value={
        'Configuration': one_change_start_function_config_in_aws,
    })
    fake_lambda_connection.update_function_configuration.configure_mock(return_value={
        'Version': 1,
    })
    fake_boto3_conn = Mock(return_value=fake_lambda_connection)

    @patch('ansible.modules.cloud.amazon.lambda.boto3_conn', fake_boto3_conn)
    def call_module():
        with pytest.raises(SystemExit):
            lda.main()
    call_module()
    assert (len(fake_boto3_conn.mock_calls) == 1), 'multiple boto connections used unexpectedly'
    assert (len(fake_lambda_connection.update_function_configuration.mock_calls) > 0), 'failed to update lambda function when configuration changed'
    assert (len(fake_lambda_connection.update_function_configuration.mock_calls) < 2), 'lambda function update called multiple times when only one time should be needed'
    assert (len(fake_lambda_connection.update_function_code.mock_calls) == 0), 'updated lambda code when no change should have happened'