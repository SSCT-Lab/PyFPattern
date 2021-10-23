def __init__(self, logging_dir, prefix=None):
    self.prefix = prefix
    try:
        from tensorboard import SummaryWriter
        self.summary_writer = SummaryWriter(logging_dir)
    except ImportError:
        logging.error('You can install tensorboard via `pip install tensorboard`.')