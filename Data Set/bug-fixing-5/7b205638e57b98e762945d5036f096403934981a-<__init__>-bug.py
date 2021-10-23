def __init__(self, project, topic, batch_max_bytes=((1024 * 1024) * 5), batch_max_latency=0.05, batch_max_messages=1000):
    settings = pubsub_v1.types.BatchSettings(max_bytes=batch_max_bytes, max_latency=batch_max_latency, max_messages=batch_max_messages)
    self.publisher = pubsub_v1.PublisherClient(settings)
    self.topic = self.publisher.topic_path(project, topic)