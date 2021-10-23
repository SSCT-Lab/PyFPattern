def build(self, is_top_level=True):
    model = self.model
    if (not ((type(model) == _keras.models.Sequential) or (type(model) == _keras.models.Model))):
        raise TypeError(('Keras layer of type %s is not supported.' % type(model)))
        self = None
        return
    for (i, layer) in enumerate(model.layers):
        in_nodes = (layer._inbound_nodes if hasattr(layer, '_inbound_nodes') else layer.inbound_nodes)
        for node in in_nodes:
            for pred in node.inbound_layers:
                if (pred.name not in self.layer_list):
                    self.layer_list.append(pred.name)
                    self.keras_layer_map[pred.name] = pred
                self._add_edge(pred.name, layer.name)
        self.layer_list.append(layer.name)
        self.keras_layer_map[layer.name] = layer
    idx = self._get_first_shared_layer()
    while (idx >= 0):
        layer = self.layer_list[idx]
        keras_layer = self.keras_layer_map[layer]
        predecessors = self.reverse_edge_map[layer]
        successors = self.edge_map[layer]
        new_layers = [((layer + '_') + str(i)) for i in range(len(predecessors))]
        self.layer_list[idx:(idx + 1)] = new_layers
        for (i, new_layer) in enumerate(new_layers):
            self.edge_map[new_layer] = []
            self.reverse_edge_map[new_layer] = []
            self.keras_layer_map[new_layer] = keras_layer
            pred = predecessors[i]
            self._add_edge(pred, new_layer)
            for succ in successors:
                self._add_edge(new_layer, succ)
        self._remove_old_edges(layer)
        self.keras_layer_map.pop(layer)
        idx = self._get_first_shared_layer()
    idx = self._get_first_embedded_model()
    while (idx >= 0):
        embedded_model = self.layer_list[idx]
        embedded_keras_model = self.keras_layer_map[embedded_model]
        embedded_graph = NetGraph(embedded_keras_model)
        embedded_graph.build(is_top_level=False)
        embedded_layer_list = embedded_graph.layer_list
        new_layer_list = []
        for embedded_layer_name in embedded_layer_list:
            new_layer_name = ((embedded_model + '_') + embedded_layer_name)
            new_layer_list.append(new_layer_name)
            self.keras_layer_map[new_layer_name] = embedded_graph.keras_layer_map[embedded_layer_name]
            embedded_successors = embedded_graph.get_successors(embedded_layer_name)
            for embed_succ_name in embedded_successors:
                new_embed_succ_name = ((embedded_model + '_') + embed_succ_name)
                self._add_edge(new_layer_name, new_embed_succ_name)
            embedded_predecessors = embedded_graph.get_predecessors(embedded_layer_name)
            for embed_pred_name in embedded_predecessors:
                new_embed_pred_name = ((embedded_model + '_') + embed_pred_name)
                self._add_edge(new_embed_pred_name, new_layer_name)
        self.layer_list[(idx + 1):(idx + 1)] = new_layer_list
        predecessors = self.get_predecessors(embedded_model)
        embedded_inputs = embedded_graph.get_input_layers()
        for (i, pred) in enumerate(predecessors):
            embed_input = embedded_inputs[i]
            new_embed_input = ((embedded_model + '_') + embed_input)
            self._add_edge(pred, new_embed_input)
        embedded_outputs = embedded_graph.get_output_layers()
        successors = self.get_successors(embedded_model)
        for (i, succ) in enumerate(successors):
            embed_output = embedded_outputs[i]
            new_embed_output = ((embedded_model + '_') + embed_output)
            self._add_edge(new_embed_output, succ)
        self._remove_layer(embedded_model)
        idx = self._get_first_embedded_model()
    self.make_input_layers()
    self.make_output_layers()
    if is_top_level:
        self.remove_skip_layers(_KERAS_SKIP_LAYERS)
        self.insert_1d_permute_layers()
        self.insert_permute_for_spatial_bn()
        self.defuse_activation()
        self.remove_internal_input_layers()