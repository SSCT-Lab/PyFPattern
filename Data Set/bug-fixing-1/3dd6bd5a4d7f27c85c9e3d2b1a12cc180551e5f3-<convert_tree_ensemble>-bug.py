

def convert_tree_ensemble(model, feature_names, target, force_32bit_float):
    'Convert a generic tree model to the protobuf spec.\n\n    This currently supports:\n      * Decision tree regression\n\n    Parameters\n    ----------\n    model: str | Booster\n        Path on disk where the XGboost JSON representation of the model is or\n        a handle to the XGboost model.\n\n    feature_names : list of strings or None\n        Names of each of the features. When set to None, the feature names are\n        extracted from the model.\n\n    target: str,\n        Name of the output column.\n\n    force_32bit_float: bool\n        If True, then the resulting CoreML model will use 32 bit floats internally.\n\n    Returns\n    -------\n    model_spec: An object of type Model_pb.\n        Protobuf representation of the model\n    '
    if (not _HAS_XGBOOST):
        raise RuntimeError('xgboost not found. xgboost conversion API is disabled.')
    import json
    import os
    feature_map = None
    if isinstance(model, (_xgboost.core.Booster, _xgboost.XGBRegressor)):
        if isinstance(model, _xgboost.XGBRegressor):
            try:
                objective = model.get_xgb_params()['objective']
            except:
                objective = None
            if (objective in ['reg:gamma', 'reg:tweedie']):
                raise ValueError(("Regression objective '%s' not supported for export." % objective))
        if isinstance(model, _xgboost.XGBRegressor):
            model = model.booster()
        if ((feature_names is None) and (model.feature_names is None)):
            raise ValueError('Feature names not present in the model. Must be provided during conversion.')
            feature_names = model.feature_names
        if (feature_names is None):
            feature_names = model.feature_names
        xgb_model_str = model.get_dump(with_stats=True, dump_format='json')
        if model.feature_names:
            feature_map = {f: i for (i, f) in enumerate(model.feature_names)}
    elif isinstance(model, str):
        if (not os.path.exists(model)):
            raise TypeError(('Invalid path %s.' % model))
        with open(model) as f:
            xgb_model_str = json.load(f)
        feature_map = {f: i for (i, f) in enumerate(feature_names)}
    else:
        raise TypeError('Unexpected type. Expecting XGBoost model.')
    mlkit_tree = _TreeEnsembleRegressor(feature_names, target)
    mlkit_tree.set_default_prediction_value(0.5)
    for (xgb_tree_id, xgb_tree_str) in enumerate(xgb_model_str):
        xgb_tree_json = json.loads(xgb_tree_str)
        recurse_json(mlkit_tree, xgb_tree_json, xgb_tree_id, node_id=0, feature_map=feature_map, force_32bit_float=force_32bit_float)
    return mlkit_tree.spec
