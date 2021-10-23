

def train(self):
    for (i, data) in enumerate(self.dataset, (self.iterations + 1)):
        (batch_input, batch_target) = data
        self.call_plugins('batch', i, batch_input, batch_target)
        input_var = Variable(batch_input, requires_grad=False)
        target_var = Variable(batch_target, requires_grad=False)
        plugin_data = [None, None]

        def forward_closure():
            batch_output = self.model(input_var)
            loss = self.criterion(batch_output, target_var)
            if (plugin_data[0] is None):
                plugin_data[0] = batch_output.data
                plugin_data[1] = loss.data
            return loss
        self.optimizer.step(forward_closure)
        self.call_plugins('iteration', i, batch_input, batch_target, *plugin_data)
        self.call_plugins('update', i, self.model)
    self.iterations += i
