def _init_splited_vars(self, slice_var_up):
    param_list = []
    grad_list = []
    param_grad_set = set()
    for (p, g) in self.params_grads:
        if ((type(p) == Parameter) and (p.trainable == False)):
            continue
        if (p.name not in param_grad_set):
            param_list.append(p)
            param_grad_set.add(p.name)
        if (g.name not in param_grad_set):
            grad_list.append(g)
            param_grad_set.add(g.name)
    self._update_dist_lookup_table_vars(param_list, grad_list, self.params_grads)
    if slice_var_up:
        grad_blocks = slice_variable(grad_list, len(self.pserver_endpoints))
        param_blocks = slice_variable(param_list, len(self.pserver_endpoints))
    else:
        grad_blocks = slice_variable(grad_list, 1)
        param_blocks = slice_variable(param_list, 1)
    assert (len(grad_blocks) == len(param_blocks))
    self.param_var_mapping = self._create_vars_from_blocklist(self.origin_program, param_blocks)
    self.grad_var_mapping = self._create_vars_from_blocklist(self.origin_program, grad_blocks, add_trainer_suffix=(self.trainer_num > 1))
    self.grad_param_mapping = dict()
    for (g, p) in zip(grad_blocks, param_blocks):
        (g_name, g_bid, _) = g.split(':')
        (p_name, p_bid, _) = p.split(':')
        self.grad_param_mapping[self.grad_var_mapping[g_name][int(g_bid)]] = self.param_var_mapping[p_name][int(p_bid)]
    self.param_grad_ep_mapping = dict()
    [self.param_grad_ep_mapping.update({
        ep: {
            'params': [],
            'grads': [],
        },
    }) for ep in self.pserver_endpoints]