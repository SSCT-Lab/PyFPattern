def test_dont_update_lambda_if_nothing_changed():
    set_module_args(base_module_args)
    (boto3_conn_double, lambda_client_double) = make_mock_connection(base_lambda_config)
    with patch.object(lda, 'boto3_conn', boto3_conn_double):
        try:
            lda.main()
        except SystemExit:
            pass
    assert (len(boto3_conn_double.mock_calls) == 1), 'multiple boto connections used unexpectedly'
    assert (len(lambda_client_double.update_function_configuration.mock_calls) == 0), 'updated lambda function when no configuration changed'
    assert (len(lambda_client_double.update_function_code.mock_calls) == 0), 'updated lambda code when no change should have happened'