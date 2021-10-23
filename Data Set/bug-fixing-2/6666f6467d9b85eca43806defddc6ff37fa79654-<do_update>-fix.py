

def do_update(self, itr, batch):
    (obss, acts, rwds, ends, nxts) = batch
    self.policy_target.arg_dict['obs'][:] = nxts
    self.policy_target.forward(is_train=False)
    next_acts = self.policy_target.outputs[0].asnumpy()
    policy_acts = self.policy.get_actions(obss)
    self.qfunc_target.arg_dict['obs'][:] = nxts
    self.qfunc_target.arg_dict['act'][:] = next_acts
    self.qfunc_target.forward(is_train=False)
    next_qvals = self.qfunc_target.outputs[0].asnumpy()
    rwds = rwds.reshape(((- 1), 1))
    ends = ends.reshape(((- 1), 1))
    ys = (rwds + (((1.0 - ends) * self.discount) * next_qvals))
    self.qfunc.update_params(obss, acts, ys)
    qfunc_loss = self.qfunc.exe.outputs[0].asnumpy()
    qvals = self.qfunc.exe.outputs[1].asnumpy()
    self.policy_executor.arg_dict['obs'][:] = obss
    self.policy_executor.arg_dict['act'][:] = policy_acts
    self.policy_executor.forward(is_train=True)
    policy_loss = self.policy_executor.outputs[0].asnumpy()
    self.policy_executor.backward()
    self.policy.update_params(self.policy_executor_grad_dict['act'])
    for (name, arr) in self.policy_target.arg_dict.items():
        if (name not in self.policy_input_shapes):
            arr[:] = (((1.0 - self.soft_target_tau) * arr[:]) + (self.soft_target_tau * self.policy.arg_dict[name][:]))
    for (name, arr) in self.qfunc_target.arg_dict.items():
        if (name not in self.qfunc_input_shapes):
            arr[:] = (((1.0 - self.soft_target_tau) * arr[:]) + (self.soft_target_tau * self.qfunc.arg_dict[name][:]))
    self.qfunc_loss_averages.append(qfunc_loss)
    self.policy_loss_averages.append(policy_loss)
    self.q_averages.append(qvals)
    self.y_averages.append(ys)
