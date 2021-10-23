

def on_error(self, trainer, exc, tb):
    'Handles the error raised during training before finalization.\n\n        This method is called when an exception is thrown during the\n        training loop, before finalize. An extension that needs\n        different error handling from finalize, can override this\n        method to handle errors.\n\n        Args:\n            trainer (Trainer): Trainer object that runs the training loop.\n            exc (Exception): arbitrary exception thrown during update loop.\n            tb (traceback): traceback object of the exception\n\n        '
    pass
