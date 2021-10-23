def get(self, key):
    cluster_name = settings.KAFKA_TOPICS[key]['cluster']
    producer = self.__producers.get(cluster_name)
    if producer:
        return producer
    from confluent_kafka import Producer
    cluster_options = settings.KAFKA_CLUSTERS[cluster_name]
    producer = self.__producers[cluster_name] = Producer(cluster_options)
    return producer