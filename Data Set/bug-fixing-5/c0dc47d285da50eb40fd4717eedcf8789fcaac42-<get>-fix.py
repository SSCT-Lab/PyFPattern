def get(self, key):
    cluster_name = settings.KAFKA_TOPICS[key]['cluster']
    producer = self.__producers.get(cluster_name)
    if producer:
        return producer
    from confluent_kafka import Producer
    cluster_options = settings.KAFKA_CLUSTERS[cluster_name]
    producer = self.__producers[cluster_name] = Producer(cluster_options)

    @atexit.register
    def exit_handler():
        pending_count = len(producer)
        if (pending_count == 0):
            return
        logger.debug('Waiting for %d messages to be flushed from %s before exiting...', pending_count, cluster_name)
        producer.flush()
    return producer