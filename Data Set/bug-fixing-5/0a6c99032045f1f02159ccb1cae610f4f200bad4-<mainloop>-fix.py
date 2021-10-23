def mainloop(self):
    while ((not EventLoop.quit) and (EventLoop.status == 'started')):
        try:
            self._mainloop()
        except BaseException as inst:
            r = ExceptionManager.handle_exception(inst)
            if (r == ExceptionManager.RAISE):
                stopTouchApp()
                raise
            else:
                pass
    Logger.info('WindowSDL: exiting mainloop and closing.')
    self.close()