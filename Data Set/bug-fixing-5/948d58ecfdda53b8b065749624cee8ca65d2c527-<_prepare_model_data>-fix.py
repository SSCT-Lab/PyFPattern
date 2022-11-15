def _prepare_model_data(self, model_test):
    onnx_home = os.path.expanduser(os.getenv('ONNX_HOME', '~/.onnx'))
    models_dir = os.getenv('ONNX_MODELS', os.path.join(onnx_home, 'models'))
    model_dir = os.path.join(models_dir, model_test.model_name)
    if (not os.path.exists(model_dir)):
        os.makedirs(model_dir)
        url = 'https://s3.amazonaws.com/download.onnx/models/{}.tar.gz'.format(model_test.model_name)
        download_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            download_file.close()
            print('Start downloading model {} from {}'.format(model_test.model_name, url))
            urlretrieve(url, download_file.name)
            print('Done')
            with tarfile.open(download_file.name) as t:
                
                import os
                
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(t, models_dir)
        except Exception as e:
            print('Failed to prepare data for model {}: {}'.format(model_test.model_name, e))
            raise
        finally:
            os.remove(download_file.name)
    return model_dir