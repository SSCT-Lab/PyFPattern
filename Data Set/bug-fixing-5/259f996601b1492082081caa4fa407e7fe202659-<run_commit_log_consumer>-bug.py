def run_commit_log_consumer(bootstrap_servers, consumer_group, commit_log_topic, partition_state_manager, synchronize_commit_group, start_event, stop_request_event):
    start_event.set()
    logging.debug('Starting commit log consumer...')
    positions = {
        
    }
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': consumer_group,
        'enable.auto.commit': 'false',
        'enable.auto.offset.store': 'true',
        'enable.partition.eof': 'false',
        'default.topic.config': {
            'auto.offset.reset': 'error',
        },
    })

    def rewind_partitions_on_assignment(consumer, assignment):
        consumer.assign([TopicPartition(i.topic, i.partition, positions.get((i.topic, i.partition), OFFSET_BEGINNING)) for i in assignment])
    consumer.subscribe([commit_log_topic], on_assign=rewind_partitions_on_assignment)
    while (not stop_request_event.is_set()):
        message = consumer.poll(1)
        if (message is None):
            continue
        error = message.error()
        if (error is not None):
            raise Exception(error)
        positions[(message.topic(), message.partition())] = (message.offset() + 1)
        (group, topic, partition, offset) = get_commit_data(message)
        if (group != synchronize_commit_group):
            logger.debug('Received consumer offsets update from %r, ignoring...', group)
            continue
        partition_state_manager.set_remote_offset(topic, partition, offset)