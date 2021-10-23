@staticmethod
def _reduction_thread_fn(queue, group_id, device_ids, reduction_streams, nccl_streams):

    def _process_batch():
        (dev_grad_batch, dev_events, job_event) = queue.get()
        dev_coalesced = []
        for (dev_id, grad_batch, event, stream) in zip(device_ids, dev_grad_batch, dev_events, reduction_streams):
            with torch.cuda.device(dev_id), torch.cuda.stream(stream):
                stream.wait_event(event)
                coalesced = _flatten_tensors(grad_batch)
                dev_coalesced.append(coalesced)
        for stream in reduction_streams:
            stream.synchronize()
        nccl.reduce(dev_coalesced, root=0, streams=nccl_streams)
        grad_batch = dev_grad_batch[0]
        coalesced = dev_coalesced[0]
        reduce_stream = reduction_streams[0]
        with torch.cuda.stream(reduce_stream):
            reduce_stream.wait_stream(nccl_streams[0])
            coalesced /= dist.get_world_size()
            dist.all_reduce(coalesced, group=group_id)
            for (grad, reduced) in zip(grad_batch, _unflatten_tensors(coalesced, grad_batch)):
                grad.copy_(reduced)
        job_event.set()
    with torch.cuda.device(device_ids[0]):
        while True:
            _process_batch()