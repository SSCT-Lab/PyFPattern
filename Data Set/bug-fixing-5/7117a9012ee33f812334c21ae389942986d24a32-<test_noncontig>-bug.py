def test_noncontig(self, test_case, module, input):
    test_case._zero_grad_parameters(module)
    test_case._zero_grad_input(input)
    with freeze_rng_state():
        output = test_case._forward(module, input)
        grad_output = output
        if isinstance(grad_output, Variable):
            grad_output = grad_output.data.clone()
        else:
            grad_output = grad_output.clone()
            output = output.clone()
        grad_output.normal_()
        d_input = deepcopy(test_case._backward(module, input, output, grad_output))
        d_param = deepcopy(test_case._get_parameters(module)[1])
    nc_input = self.noncontiguize(input)
    nc_grad_output = self.noncontiguize(grad_output)
    for (contig_i, contig_g) in product((True, False), repeat=2):
        i = (input if contig_i else nc_input)
        go = (grad_output if contig_g else nc_grad_output)
        test_case._zero_grad_parameters(module)
        test_case._zero_grad_input(i)
        with freeze_rng_state():
            try:
                out = test_case._forward(module, i)
            except Exception:
                continue
            grad = test_case._backward(module, i, out, go)
            test_case.assertEqual(out, output)
            test_case.assertEqual(grad, d_input)
            test_case.assertEqual(test_case._get_parameters(module)[1], d_param)