

def _model_dir(self, model):
    caffe2_home = os.path.expanduser(os.getenv('CAFFE2_HOME', '~/.caffe2'))
    models_dir = os.getenv('CAFFE2_MODELS', os.path.join(caffe2_home, 'models'))
    return os.path.join(models_dir, model)
