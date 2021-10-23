def __getstate__(self):
    attrs = copy.copy(self.__dict__)
    del attrs['_grad_accs'], attrs['_reduction_queues'], attrs['_reduction_streams'], attrs['_reduction_threads'], attrs['_nccl_streams'], attrs['_default_streams']
    return attrs