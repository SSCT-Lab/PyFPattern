def build(self, input_shape=None):
    if ((not self.inputs) or (not self.outputs)):
        raise Exception('Sequential model cannot be built: model is empty. Add some layers first.')
    self.model = Model(self.inputs, self.outputs[0], name=(self.name + '_model'))
    self.supports_masking = self.model.supports_masking
    self._output_mask_cache = self.model._output_mask_cache
    self._output_tensor_cache = self.model._output_tensor_cache
    self._output_shape_cache = self.model._output_shape_cache
    self.input_layers = self.model.input_layers
    self.input_layers_node_indices = self.model.input_layers_node_indices
    self.input_layers_tensor_indices = self.model.input_layers_tensor_indices
    self.output_layers = self.model.output_layers
    self.output_layers_node_indices = self.model.output_layers_node_indices
    self.output_layers_tensor_indices = self.model.output_layers_tensor_indices
    self.nodes_by_depth = self.model.nodes_by_depth
    self.container_nodes = self.model.container_nodes
    self.output_names = self.model.output_names
    self.input_names = self.model.input_names
    self.model.callback_model = self
    self.built = True