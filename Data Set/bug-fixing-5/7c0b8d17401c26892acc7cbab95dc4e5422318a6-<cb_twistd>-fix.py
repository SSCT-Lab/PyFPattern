def cb_twistd(self, *la):
    if self.running:
        IServiceCollection(self.app).stopService()
        self.running = False
    else:
        sys.path.insert(0, os.path.abspath(os.getcwd()))
        sys.argv = TWISTD.split(' ')
        config = ServerOptions()
        config.parseOptions()
        self.app = AndroidApplicationRunner(config).run()
        self.running = True