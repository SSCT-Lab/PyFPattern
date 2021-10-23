def parse(self):
    ' create an options parser for bin/ansible '
    self.parser = CLI.base_parser(usage=('usage: %%prog [%s] [--help] [options] ...' % '|'.join(self.VALID_ACTIONS)), epilog=("\nSee '%s <command> --help' for more information on a specific command.\n\n" % os.path.basename(sys.argv[0])))
    self.parser.add_option('-s', '--server', dest='api_server', default=C.GALAXY_SERVER, help='The API server destination')
    self.parser.add_option('-c', '--ignore-certs', action='store_true', dest='ignore_certs', default=C.GALAXY_IGNORE_CERTS, help='Ignore SSL certificate validation errors.')
    self.set_action()
    super(GalaxyCLI, self).parse()
    display.verbosity = self.options.verbosity
    self.galaxy = Galaxy(self.options)