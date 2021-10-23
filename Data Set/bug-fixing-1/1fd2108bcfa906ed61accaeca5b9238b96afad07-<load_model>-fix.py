

def load_model(filepath, custom_objects={
    
}):

    def deserialize(obj):
        if (type(obj) is list):
            deserialized = []
            for value in obj:
                if (value in custom_objects):
                    deserialized.append(custom_objects[value])
                else:
                    deserialized.append(value)
            return deserialized
        if (type(obj) is dict):
            deserialized = {
                
            }
            for (key, value) in obj.items():
                if (value in custom_objects):
                    deserialized[key] = custom_objects[value]
                else:
                    deserialized[key] = value
            return deserialized
        if (obj in custom_objects):
            return custom_objects[obj]
        return obj
    import h5py
    f = h5py.File(filepath, mode='r')
    model_config = f.attrs.get('model_config')
    if (model_config is None):
        raise ValueError('No model found in config file.')
    model_config = json.loads(model_config.decode('utf-8'))
    model = model_from_config(model_config, custom_objects=custom_objects)
    model.load_weights_from_hdf5_group(f['model_weights'])
    training_config = f.attrs.get('training_config')
    if (training_config is None):
        warnings.warn('No training configuration found in save file: the model was *not* compiled. Compile it manually.')
        f.close()
        return model
    training_config = json.loads(training_config.decode('utf-8'))
    optimizer_config = training_config['optimizer_config']
    optimizer = optimizer_from_config(optimizer_config, custom_objects=custom_objects)
    loss = deserialize(training_config['loss'])
    metrics = deserialize(training_config['metrics'])
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
        model.optimizer.set_weights(optimizer_weight_values)
    f.close()
    return model
