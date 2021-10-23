

def relay(self, consumer_group, commit_log_topic, synchronize_commit_group, commit_batch_size=100, initial_offset_reset='latest'):
    logger.debug('Starting relay...')
    consumer = SynchronizedConsumer(bootstrap_servers=self.producer_configuration['bootstrap.servers'], consumer_group=consumer_group, commit_log_topic=commit_log_topic, synchronize_commit_group=synchronize_commit_group, initial_offset_reset=initial_offset_reset)
    owned_partition_offsets = {
        
    }

    def on_assign(consumer, partitions):
        logger.debug('Received partition assignment: %r', partitions)
        for i in partitions:
            if (i.offset == OFFSET_INVALID):
                updated_offset = None
            elif (i.offset < 0):
                raise Exception(('Received unexpected negative offset during partition assignment: %r' % (i,)))
            else:
                updated_offset = i.offset
            key = (i.topic, i.partition)
            previous_offset = owned_partition_offsets.get(key, None)
            if ((previous_offset is not None) and (previous_offset != updated_offset)):
                logger.warning('Received new offset for owned partition %r, will overwrite previous stored offset %r with %r.', key, previous_offset, updated_offset)
            owned_partition_offsets[key] = updated_offset

    def on_revoke(consumer, partitions):
        logger.debug('Revoked partition assignment: %r', partitions)
        offsets_to_commit = []
        for i in partitions:
            key = (i.topic, i.partition)
            try:
                offset = owned_partition_offsets.pop(key)
            except KeyError:
                logger.warning('Received unexpected partition revocation for unowned partition: %r', i, exc_info=True)
                continue
            if (offset is None):
                logger.debug('Skipping commit of unprocessed partition: %r', i)
                continue
            offsets_to_commit.append(TopicPartition(i.topic, i.partition, offset))
        if offsets_to_commit:
            logger.debug('Committing offset(s) for %s revoked partition(s): %r', len(offsets_to_commit), offsets_to_commit)
            consumer.commit(offsets=offsets_to_commit, asynchronous=False)
    consumer.subscribe([self.publish_topic], on_assign=on_assign, on_revoke=on_revoke)

    def commit_offsets():
        offsets_to_commit = []
        for ((topic, partition), offset) in owned_partition_offsets.items():
            if (offset is None):
                logger.debug('Skipping commit of unprocessed partition: %r', (topic, partition))
                continue
            offsets_to_commit.append(TopicPartition((topic, partition, offset)))
        if offsets_to_commit:
            logger.debug('Committing offset(s) for %s owned partition(s): %r', len(offsets_to_commit), offsets_to_commit)
            consumer.commit(offsets=offsets_to_commit, asynchronous=False)
    try:
        i = 0
        while True:
            message = consumer.poll(0.1)
            if (message is None):
                continue
            error = message.error()
            if (error is not None):
                raise Exception(error)
            key = (message.topic(), message.partition())
            if (key not in owned_partition_offsets):
                logger.warning('Skipping message for unowned partition: %r', key)
                continue
            i = (i + 1)
            owned_partition_offsets[key] = (message.offset() + 1)
            payload = parse_event_message(message.value())
            if (payload is not None):
                post_process_group.delay(**payload)
            if ((i % commit_batch_size) == 0):
                commit_offsets()
    except KeyboardInterrupt:
        pass
    logger.debug('Committing offsets and closing consumer...')
    commit_offsets()
    consumer.close()
