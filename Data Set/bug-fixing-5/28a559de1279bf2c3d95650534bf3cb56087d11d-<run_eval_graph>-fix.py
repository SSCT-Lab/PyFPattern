def run_eval_graph(self, sampled_rate=None, cached_id=0):
    '\n        Evaluate the current mode in context.\n        Args:\n            sampled_rate(float): The sampled rate used to sample partial data\n            for evaluation. None means using all data in eval_reader. default: None.\n            cached_id(int): The id of dataset sampled. Evaluations with same\n                            cached_id use the same sampled dataset. default: 0.\n        '
    _logger.info('Running evaluation')
    assert (self.eval_graph is not None)
    assert (self.eval_reader is not None)
    eval_graph = self.eval_graph.clone(for_test=True)
    executor = SlimGraphExecutor(self.place)
    results = []
    batch_id = 0
    s_time = time.time()
    reader = self.eval_reader
    if sampled_rate:
        assert (not isinstance(reader, Variable))
        assert (sampled_rate > 0)
        assert (self.cache_path is not None)
        _logger.info('sampled_rate: {}; cached_id: {}'.format(sampled_rate, cached_id))
        reader = cached_reader(reader, sampled_rate, self.cache_path, cached_id)
    if (isinstance(reader, Variable) or (isinstance(reader, PyReader) and (not reader.iterable))):
        reader.start()
        try:
            while True:
                result = executor.run(eval_graph, self.scope)
                result = [np.mean(r) for r in result]
                results.append(result)
                if ((batch_id % 20) == 0):
                    _logger.info('batch-{}; {}={}'.format(batch_id, eval_graph.out_nodes.keys(), result))
                batch_id += 1
        except EOFException:
            reader.reset()
    else:
        for data in reader():
            result = executor.run(eval_graph, self.scope, data=data)
            result = [np.mean(r) for r in result]
            results.append(result)
            if ((batch_id % 20) == 0):
                _logger.info('batch-{}; {}={}'.format(batch_id, eval_graph.out_nodes.keys(), result))
            batch_id += 1
    result = np.mean(np.array(results), axis=0)
    _logger.info('Final eval result: {}={}'.format(eval_graph.out_nodes.keys(), result))
    if (not isinstance(result, Iterable)):
        result = [result]
    _logger.info('Finish evaluation')
    return (result, eval_graph.out_nodes.keys())