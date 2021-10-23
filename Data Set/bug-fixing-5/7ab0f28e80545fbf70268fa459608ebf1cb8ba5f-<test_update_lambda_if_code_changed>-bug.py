def test_update_lambda_if_code_changed(monkeypatch):
    fake_lambda_connection = MagicMock()
    fake_lambda_connection.get_function.configure_mock(return_value={
        'Configuration': code_change_start_function_config_in_aws,
    })
    fake_lambda_connection.update_function_configuration.configure_mock(return_value={
        'Version': 1,
    })
    fake_boto3_conn = Mock(return_value=fake_lambda_connection)
    set_module_args(base_module_args)

    @patch('ansible.modules.cloud.amazon.lambda.boto3_conn', fake_boto3_conn)
    def call_module():
        with pytest.raises(SystemExit):
            lda.main()
    call_module()
    assert (len(fake_boto3_conn.mock_calls) == 1), 'multiple boto connections used unexpectedly'
    assert (len(fake_lambda_connection.update_function_configuration.mock_calls) == 0), 'unexpectedly updatede lambda configuration when only code changed'
    assert (len(fake_lambda_connection.update_function_configuration.mock_calls) < 2), 'lambda function update called multiple times when only one time should be needed'
    assert (len(fake_lambda_connection.update_function_code.mock_calls) > 1), 'failed to update lambda function when code changed'
    assert (len(fake_lambda_connection.update_function_code.mock_calls) < 3), 'lambda function code update called multiple times when only one time should be needed'