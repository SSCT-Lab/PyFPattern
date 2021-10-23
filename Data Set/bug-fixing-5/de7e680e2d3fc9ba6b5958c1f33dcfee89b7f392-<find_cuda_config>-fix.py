def find_cuda_config():
    'Returns a dictionary of CUDA library and header file paths.'
    libraries = [argv.lower() for argv in sys.argv[1:]]
    cuda_version = os.environ.get('TF_CUDA_VERSION', '')
    base_paths = _list_from_env('TF_CUDA_PATHS', _get_default_cuda_paths(cuda_version))
    base_paths = [path for path in base_paths if os.path.exists(path)]
    result = {
        
    }
    if ('cuda' in libraries):
        cuda_paths = _list_from_env('CUDA_TOOLKIT_PATH', base_paths)
        result.update(_find_cuda_config(cuda_paths, cuda_version))
        cuda_version = result['cuda_version']
        cublas_paths = base_paths
        if (tuple((int(v) for v in cuda_version.split('.'))) < (10, 1)):
            cublas_paths = cuda_paths
        cublas_version = os.environ.get('TF_CUBLAS_VERSION', '')
        result.update(_find_cublas_config(cublas_paths, cublas_version, cuda_version))
    if ('cudnn' in libraries):
        cudnn_paths = _get_legacy_path('CUDNN_INSTALL_PATH', base_paths)
        cudnn_version = os.environ.get('TF_CUDNN_VERSION', '')
        result.update(_find_cudnn_config(cudnn_paths, cudnn_version))
    if ('nccl' in libraries):
        nccl_paths = _get_legacy_path('NCCL_INSTALL_PATH', base_paths)
        nccl_version = os.environ.get('TF_NCCL_VERSION', '')
        result.update(_find_nccl_config(nccl_paths, nccl_version))
    if ('tensorrt' in libraries):
        tensorrt_paths = _get_legacy_path('TENSORRT_INSTALL_PATH', base_paths)
        tensorrt_version = os.environ.get('TF_TENSORRT_VERSION', '')
        result.update(_find_tensorrt_config(tensorrt_paths, tensorrt_version))
    for (k, v) in result.items():
        if (k.endswith('_dir') or k.endswith('_path')):
            result[k] = _normalize_path(v)
    return result