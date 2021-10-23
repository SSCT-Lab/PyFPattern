

def batch(reader, batch_size, drop_last=False):
    '\n    Create a batched reader.\n\n    :param reader: the data reader to read from.\n    :type reader: callable\n    :param batch_size: size of each mini-batch\n    :type batch_size: int\n    :param drop_last: drop the last batch, if the size of last batch is not equal to batch_size.\n    :type drop_last: bool\n    :return: the batched reader.\n    :rtype: callable\n    '

    def batch_reader():
        r = reader()
        b = []
        for instance in r:
            b.append(instance)
            if (len(b) == batch_size):
                (yield b)
                b = []
        if ((drop_last == False) and (len(b) != 0)):
            (yield b)
    batch_size = int(batch_size)
    if (batch_size <= 0):
        raise ValueError('batch_size should be a positive integeral value, but got batch_size={}'.format(batch_size))
    return batch_reader
