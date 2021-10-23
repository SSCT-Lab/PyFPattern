def default_collate(batch):
    'Puts each data field into a tensor with outer dimension batch size'
    if torch.is_tensor(batch[0]):
        return torch.stack(batch, 0)
    elif (type(batch[0]).__module__ == 'numpy'):
        return torch.stack([torch.from_numpy(b) for b in batch], 0)
    elif isinstance(batch[0], int):
        return torch.LongTensor(batch)
    elif isinstance(batch[0], float):
        return torch.DoubleTensor(batch)
    elif isinstance(batch[0], string_classes):
        return batch
    elif isinstance(batch[0], collections.Iterable):
        transposed = zip(*batch)
        return [default_collate(samples) for samples in transposed]
    raise TypeError('batch must contain tensors, numbers, or lists; found {}'.format(type(batch[0])))