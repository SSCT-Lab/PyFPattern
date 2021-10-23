

@tf_export(v1=['logging.warn'])
def warn(msg, *args, **kwargs):
    get_logger().warn(msg, *args, **kwargs)
