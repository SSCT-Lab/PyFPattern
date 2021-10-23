def test_manage_state_adds_missing_permissions():
    lambda_client_double = MagicMock()
    lambda_client_double.get_policy.side_effect = resource_not_found_e
    fake_module_params = copy.deepcopy(fake_module_params_present)
    module_double.params = fake_module_params
    lambda_policy.manage_state(module_double, lambda_client_double)
    assert (lambda_client_double.get_policy.call_count > 0)
    assert (lambda_client_double.add_permission.call_count > 0)
    lambda_client_double.remove_permission.assert_not_called()