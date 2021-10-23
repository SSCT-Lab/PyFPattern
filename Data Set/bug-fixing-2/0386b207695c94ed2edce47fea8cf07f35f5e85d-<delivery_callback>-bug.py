

def delivery_callback(self, error, message):
    logger.warning('Could not publish event (error: %s): %r', error, message)
