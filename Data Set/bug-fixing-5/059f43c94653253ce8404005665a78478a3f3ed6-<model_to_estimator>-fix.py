@tf_export('keras.estimator.model_to_estimator')
def model_to_estimator(keras_model=None, keras_model_path=None, custom_objects=None, model_dir=None, config=None):
    'Constructs an `Estimator` instance from given keras model.\n\n  For usage example, please see\n  @{$programmers_guide/estimators$creating_estimators_from_keras_models}.\n\n  Args:\n    keras_model: Keras model in memory.\n    keras_model_path: Directory to a keras model on disk.\n    custom_objects: Dictionary for custom objects.\n    model_dir: Directory to save Estimator model parameters, graph and etc.\n    config: Configuration object.\n\n  Returns:\n    An Estimator from given keras model.\n\n  Raises:\n    ValueError: if neither keras_model nor keras_model_path was given.\n    ValueError: if both keras_model and keras_model_path was given.\n    ValueError: if the keras_model_path is a GCS URI.\n    ValueError: if keras_model has not been compiled.\n  '
    if ((not keras_model) and (not keras_model_path)):
        raise ValueError('Either `keras_model` or `keras_model_path` needs to be provided.')
    if (keras_model and keras_model_path):
        raise ValueError('Please specity either `keras_model` or `keras_model_path`, but not both.')
    if (not keras_model):
        if (keras_model_path.startswith('gs://') or ('storage.googleapis.com' in keras_model_path)):
            raise ValueError(('%s is not a local path. Please copy the model locally first.' % keras_model_path))
        logging.info('Loading models from %s', keras_model_path)
        keras_model = models.load_model(keras_model_path)
    else:
        logging.info('Using the Keras model provided.')
        keras_model = keras_model
    if ((not hasattr(keras_model, 'optimizer')) or (not keras_model.optimizer)):
        raise ValueError('The given keras model has not been compiled yet. Please compile first before calling `model_to_estimator`.')
    if isinstance(config, dict):
        config = run_config_lib.RunConfig(**config)
    keras_model_fn = _create_keras_model_fn(keras_model, custom_objects)
    estimator = estimator_lib.Estimator(keras_model_fn, model_dir=model_dir, config=config)
    if _any_variable_initialized():
        keras_weights = keras_model.get_weights()
        if estimator._session_config.HasField('gpu_options'):
            logging.warning('The Keras backend session has already been set. The _session_config passed to model_to_estimator will not be used.')
    else:
        sess = session.Session(config=estimator._session_config)
        K.set_session(sess)
        keras_weights = None
    if keras_model._is_graph_network:
        _save_first_checkpoint(keras_model, estimator, custom_objects, keras_weights)
    elif keras_model.built:
        logging.warning("You are creating an Estimator from a Keras model manually subclassed from `Model`, that was already called on some inputs (and thus already had weights). We are currently unable to preserve the model's state (its weights) as part of the estimator in this case. Be warned that the estimator has been created using a freshly initialized version of your model.\nNote that this doesn't affect the state of the model instance you passed as `keras_model` argument.")
    return estimator