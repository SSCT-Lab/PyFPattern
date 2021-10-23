

def load_model(filepath, custom_objects=None, compile=True):
    'Loads a model saved via `save_model`.\n\n    # Arguments\n        filepath: String, path to the saved model.\n        custom_objects: Optional dictionary mapping names\n            (strings) to custom classes or functions to be\n            considered during deserialization.\n        compile: Boolean, whether to compile the model\n            after loading.\n\n    # Returns\n        A Keras model instance. If an optimizer was found\n        as part of the saved model, the model is already\n        compiled. Otherwise, the model is uncompiled and\n        a warning will be displayed. When `compile` is set\n        to False, the compilation is omitted without any\n        warning.\n\n    # Raises\n        ImportError: if h5py is not available.\n        ValueError: In case of an invalid savefile.\n    '
    if (h5py is None):
        raise ImportError('`load_model` requires h5py.')
    if (not custom_objects):
        custom_objects = {
            
        }

    def convert_custom_objects(obj):
        'Handles custom object lookup.\n\n        # Arguments\n            obj: object, dict, or list.\n\n        # Returns\n            The same structure, where occurrences\n                of a custom object name have been replaced\n                with the custom object.\n        '
        if isinstance(obj, list):
            deserialized = []
            for value in obj:
                deserialized.append(convert_custom_objects(value))
            return deserialized
        if isinstance(obj, dict):
            deserialized = {
                
            }
            for (key, value) in obj.items():
                deserialized[key] = convert_custom_objects(value)
            return deserialized
        if (obj in custom_objects):
            return custom_objects[obj]
        return obj
    with h5py.File(filepath, mode='r') as f:
        model_config = f.attrs.get('model_config')
        if (model_config is None):
            raise ValueError('No model found in config file.')
        model_config = json.loads(model_config.decode('utf-8'))
        model = model_from_config(model_config, custom_objects=custom_objects)
        topology.load_weights_from_hdf5_group(f['model_weights'], model.layers)
        if (not compile):
            return model
        training_config = f.attrs.get('training_config')
        if (training_config is None):
            warnings.warn('No training configuration found in save file: the model was *not* compiled. Compile it manually.')
            return model
        training_config = json.loads(training_config.decode('utf-8'))
        optimizer_config = training_config['optimizer_config']
        optimizer = optimizers.deserialize(optimizer_config, custom_objects=custom_objects)
        loss = convert_custom_objects(training_config['loss'])
        metrics = convert_custom_objects(training_config['metrics'])
        sample_weight_mode = training_config['sample_weight_mode']
        loss_weights = training_config['loss_weights']
        model.compile(optimizer=optimizer, loss=loss, metrics=metrics, loss_weights=loss_weights, sample_weight_mode=sample_weight_mode)
        if ('optimizer_weights' in f):
            if isinstance(model, Sequential):
                model.model._make_train_function()
            else:
                model._make_train_function()
            optimizer_weights_group = f['optimizer_weights']
            optimizer_weight_names = [n.decode('utf8') for n in optimizer_weights_group.attrs['weight_names']]
            optimizer_weight_values = [optimizer_weights_group[n] for n in optimizer_weight_names]
            try:
                model.optimizer.set_weights(optimizer_weight_values)
            except ValueError:
                warnings.warn('Error in loading the saved optimizer state. As a result, your model is starting with a freshly initialized optimizer.')
    return model
