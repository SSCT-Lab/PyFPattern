

def cached_reader(reader, sampled_rate, cache_path, cached_id):
    '\n    Sample partial data from reader and cache them into local file system.\n    Args:\n        reader: Iterative data source.\n        sampled_rate(float): The sampled rate used to sample partial data for evaluation. None means using all data in eval_reader. default: None.\n        cache_path(str): The path to cache the sampled data.\n        cached_id(int): The id of dataset sampled. Evaluations with same cached_id use the same sampled dataset. default: 0.\n    '
    np.random.seed(cached_id)
    cache_path = os.path.join(cache_path, str(cached_id))
    _logger.debug('read data from: {}'.format(cache_path))

    def s_reader():
        if os.path.isdir(cache_path):
            for file_name in open(os.path.join(cache_path, 'list')):
                (yield np.load(os.path.join(cache_path, file_name.strip())))
        else:
            os.makedirs(cache_path)
            list_file = open(os.path.join(cache_path, 'list'), 'w')
            batch = 0
            dtype = None
            for data in reader():
                if ((batch == 0) or (np.random.uniform() < sampled_rate)):
                    np.save(os.path.join(cache_path, ('batch' + str(batch))), data)
                    list_file.write((('batch' + str(batch)) + '.npy\n'))
                    batch += 1
                    (yield data)
    return s_reader
