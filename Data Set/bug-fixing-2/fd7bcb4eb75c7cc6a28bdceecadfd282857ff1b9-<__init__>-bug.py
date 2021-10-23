

def __init__(self, hparam_def=None, model_structure=None, **kwargs):
    "Create an instance of `HParams` from keyword arguments.\n\n    The keyword arguments specify name-values pairs for the hyperparameters.\n    The parameter types are inferred from the type of the values passed.\n\n    The parameter names are added as attributes of `HParams` object, so they\n    can be accessed directly with the dot notation `hparams._name_`.\n\n    Example:\n\n    ```python\n    # Define 3 hyperparameters: 'learning_rate' is a float parameter,\n    # 'num_hidden_units' an integer parameter, and 'activation' a string\n    # parameter.\n    hparams = tf.HParams(\n        learning_rate=0.1, num_hidden_units=100, activation='relu')\n\n    hparams.activation ==> 'relu'\n    ```\n\n    Note that a few names are reserved and cannot be used as hyperparameter\n    names.  If you use one of the reserved name the constructor raises a\n    `ValueError`.\n\n    Args:\n      hparam_def: Serialized hyperparameters, encoded as a hparam_pb2.HParamDef\n        protocol buffer. If provided, this object is initialized by\n        deserializing hparam_def.  Otherwise **kwargs is used.\n      model_structure: An instance of ModelStructure, defining the feature\n        crosses to be used in the Trial.\n      **kwargs: Key-value pairs where the key is the hyperparameter name and\n        the value is the value for the parameter.\n\n    Raises:\n      ValueError: If both `hparam_def` and initialization values are provided,\n        or if one of the arguments is invalid.\n\n    "
    self._hparam_types = {
        
    }
    self._model_structure = model_structure
    if hparam_def:
        self._init_from_proto(hparam_def)
        if kwargs:
            raise ValueError('hparam_def and initialization values are mutually exclusive')
    else:
        for (name, value) in six.iteritems(kwargs):
            self.add_hparam(name, value)
