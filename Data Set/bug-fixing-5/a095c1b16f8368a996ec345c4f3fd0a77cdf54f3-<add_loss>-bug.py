def add_loss(self, losses, inputs=None):
    "Add losses to the layer.\n\n        The loss may potentially be conditional on some inputs tensors,\n        for instance activity losses are conditional on the layer's inputs.\n\n        # Arguments\n            losses: loss tensor or list of loss tensors\n                to add to the layer.\n            inputs: input tensor or list of inputs tensors to mark\n                the losses as conditional on these inputs.\n                If None is passed, the loss is assumed unconditional\n                (e.g. L2 weight regularization, which only depends\n                on the layer's weights variables, not on any inputs tensors).\n        "
    if ((losses is None) or (losses == [])):
        return
    losses = _to_list(losses)
    if hasattr(self, '_losses'):
        self._losses += losses
    if (isinstance(input, list) and (inputs == [])):
        inputs = None
    if (inputs is not None):
        inputs_hash = _object_list_uid(inputs)
    else:
        inputs_hash = None
    if (inputs_hash not in self._per_input_losses):
        self._per_input_losses[inputs_hash] = []
    self._per_input_losses[inputs_hash] += losses