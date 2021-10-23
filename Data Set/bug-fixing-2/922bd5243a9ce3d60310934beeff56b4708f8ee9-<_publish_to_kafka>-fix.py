

def _publish_to_kafka(self, request, project_config):
    '\n        Sends raw event data to Kafka for later offline processing.\n        '
    try:
        raw_event_sample_rate = options.get('kafka-publisher.raw-event-sample-rate')
        if (raw_event_sample_rate == 0):
            return
        data = request.body
        if ((not data) or (len(data) > options.get('kafka-publisher.max-event-size'))):
            return
        if (random.random() >= raw_event_sample_rate):
            return
        meta = {
            
        }
        for (key, value) in request.META.items():
            try:
                json.dumps([key, value])
                meta[key] = value
            except (TypeError, ValueError):
                pass
        meta['SENTRY_API_VIEW_NAME'] = self.__class__.__name__
        kafka_publisher.publish(channel=getattr(settings, 'KAFKA_RAW_EVENTS_PUBLISHER_TOPIC', 'raw-store-events'), value=json.dumps([meta, base64.b64encode(data)]))
    except Exception as e:
        logger.debug('Cannot publish event to Kafka: {}'.format(e.message))
