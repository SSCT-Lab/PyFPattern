

@tf_export('tpu.experimental.initialize_tpu_system')
def initialize_tpu_system(cluster_resolver=None):
    'Initialize the TPU devices.\n\n  Args:\n    cluster_resolver: A tf.distribute.cluster_resolver.TPUClusterResolver,\n        which provides information about the TPU cluster.\n  Returns:\n    The tf.tpu.Topology object for the topology of the TPU cluster.\n\n  Raises:\n    RuntimeError: If no TPU devices found for eager execution.\n  '
    job = None
    if (cluster_resolver is None):
        if context.executing_eagerly():
            curr_device = device.DeviceSpec.from_string(context.context().device_name)
            if (curr_device.job is not None):
                job = '{}/replica:0/task:0'.format(curr_device.job)
        cluster_resolver = TPUClusterResolver('')
    assert isinstance(cluster_resolver, TPUClusterResolver)
    tpu_name = compat.as_text(cluster_resolver._tpu)
    if (tpu_name in _INITIALIZED_TPU_SYSTEMS):
        logging.warning('TPU system %s has already been initialized. Reinitializing the TPU can cause previously created variables on TPU to be lost.', tpu_name)
    logging.info('Initializing the TPU system: %s', tpu_name)
    if context.executing_eagerly():
        if (tpu_name not in _LOCAL_MASTERS):
            job = '{}/replica:0/task:0'.format(cluster_resolver.get_job_name())

        @function.defun
        def _tpu_init_fn():
            return tpu.initialize_system(job=job)
        with ops.device(tpu._tpu_system_device_name(job)):
            output = _tpu_init_fn()
        logging.info('Clearing out eager caches')
        context.context()._clear_caches()
        serialized_topology = output.numpy()
        context.context().mirroring_policy = context.MIRRORING_ALL
    else:
        master = cluster_resolver.master()
        cluster_spec = cluster_resolver.cluster_spec()
        session_config = config_pb2.ConfigProto(allow_soft_placement=True)
        if cluster_spec:
            session_config.cluster_def.CopyFrom(cluster_spec.as_cluster_def())
        with ops.Graph().as_default():
            with session_lib.Session(config=session_config, target=master) as sess:
                serialized_topology = sess.run(tpu.initialize_system())
    logging.info('Finished initializing TPU system.')
    tpu_topology = topology.Topology(serialized=serialized_topology)
    _INITIALIZED_TPU_SYSTEMS[tpu_name] = tpu_topology
    return tpu_topology
