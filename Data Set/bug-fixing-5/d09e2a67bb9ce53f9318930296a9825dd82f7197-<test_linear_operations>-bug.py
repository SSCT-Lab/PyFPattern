def test_linear_operations(self):
    check_two_tensor_operation('dot', (4, 2), (2, 4))
    check_two_tensor_operation('dot', (4, 2), (5, 2, 3))
    check_two_tensor_operation('batch_dot', (4, 2, 3), (4, 5, 3), axes=((2,), (2,)))
    check_single_tensor_operation('transpose', (4, 2))