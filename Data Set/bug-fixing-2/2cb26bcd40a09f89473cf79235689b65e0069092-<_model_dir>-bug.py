

def _model_dir(self, model):
    caffe2_home = os.path.expanduser(os.getenv('ONNX_HOME', '~/.caffe2'))
    models_dir = os.getenv('ONNX_MODELS', os.path.join(caffe2_home, 'models'))
    return os.path.join(models_dir, model)
