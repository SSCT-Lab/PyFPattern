def relay(self, consumer_group, commit_log_topic, synchronize_commit_group, commit_batch_size=100, initial_offset_reset='latest'):
    consumer = SynchronizedConsumer(bootstrap_servers=self.producer_configuration['bootstrap.servers'], consumer_group=consumer_group, commit_log_topic=commit_log_topic, synchronize_commit_group=synchronize_commit_group, initial_offset_reset=initial_offset_reset)
    consumer.subscribe([self.publish_topic])
    offsets = {
        
    }

    def commit_offsets():
        consumer.commit(offsets=[TopicPartition(topic, partition, offset) for ((topic, partition), offset) in offsets.items()], asynchronous=False)
    try:
        i = 0
        while True:
            message = consumer.poll(0.1)
            if (message is None):
                continue
            error = message.error()
            if (error is not None):
                raise Exception(error)
            i = (i + 1)
            offsets[(message.topic(), message.partition())] = (message.offset() + 1)
            payload = parse_event_message(message.value())
            if (payload is not None):
                post_process_group.delay(**payload)
            if ((i % commit_batch_size) == 0):
                commit_offsets()
    except KeyboardInterrupt:
        pass
    logger.info('Committing offsets and closing consumer...')
    if offsets:
        commit_offsets()
    consumer.close()