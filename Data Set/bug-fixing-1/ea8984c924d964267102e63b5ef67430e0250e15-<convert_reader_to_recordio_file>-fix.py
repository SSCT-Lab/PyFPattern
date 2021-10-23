

def convert_reader_to_recordio_file(filename, reader_creator, feeder, compressor=core.RecordIOWriter.Compressor.Snappy, max_num_records=1000, feed_order=None):
    '\n    Convert a Python Reader to a recordio file.\n\n    Examples:\n\n        >>> import paddle.fluid as fluid\n        >>> import paddle.dataset.mnist as mnist\n        >>> import paddle\n        >>>\n        >>> tmp_program = fluid.Program()\n        >>> with fluid.program_guard(tmp_program):\n        >>>     img = fluid.layers.data(name=\'img\', shape=[784])\n        >>>     label = fluid.layers.data(name=\'label\', shape=[1], dtype=\'int64\')\n        >>> feeder = fluid.DataFeeder(feed_list=[img, label], place=fluid.CPUPlace())\n        >>> # mnist.recordio will be generated in current directory\n        >>> fluid.recordio_writer.convert_reader_to_recordio_file(\n        >>>                     filename="mnist.recordio",\n        >>>                     reader_creator=paddle.batch(mnist.train(), batch_size=32),\n        >>>                     feeder=feeder)\n\n    Args:\n        filename(str): The recordio filename.\n        reader_creator(callable): The Python Reader Creator. See\n            :ref:`api_guide_python_reader`.\n        feeder(DataFeeder): The DataFeeder instance. Used to convert\n            :code:`reader_creator` to :code: `lod_tensor`\n        compressor: Must in fluid.core.RecordIOWriter.Compressor.Snappy or\n            fluid.core.RecordIOWriter.Compressor.NoCompress. Use :code:`Snappy`\n            by default.\n        max_num_records(int): Maximum number of records in one chuck. Each record\n            is each return value from reader function\n        feed_order(list): The order of variable names that the reader returns\n\n    Returns:\n        int: the number of record that saved.\n    '
    if (feed_order is None):
        feed_order = feeder.feed_names
    counter = 0
    with create_recordio_writer(filename, compressor, max_num_records) as writer:
        for batch in reader_creator():
            res = feeder.feed(batch)
            for each in feed_order:
                writer.append_tensor(res[each])
            writer.complete_append_tensor()
            counter += 1
    return counter
