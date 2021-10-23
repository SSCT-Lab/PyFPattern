def _publish_to_kafka(self, request, project_config):
    '\n        Sends raw event data to Kafka for later offline processing.\n        '
    try:
        data = request.body
        max_event_size = options.get('kafka-publisher.raw-event-sample-rate')
        if ((not data) or (max_event_size is None) or (len(data) > max_event_size)):
            return
        raw_event_sample_rate = options.get('kafka-publisher.max-event-size')
        if ((raw_event_sample_rate is None) or (random.random() >= raw_event_sample_rate)):
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