

def main(unused_argv=None):
    logdir = os.path.expanduser(FLAGS.logdir)
    event_file = os.path.expanduser(FLAGS.event_file)
    if FLAGS.debug:
        logging.set_verbosity(logging.DEBUG)
        logging.info('TensorBoard is in debug mode.')
    if FLAGS.inspect:
        logging.info('Not bringing up TensorBoard, but inspecting event files.')
        efi.inspect(logdir, event_file, FLAGS.tag)
        return 0
    if (not logdir):
        msg = 'A logdir must be specified. Run `tensorboard --help` for details and examples.'
        logging.error(msg)
        print(msg)
        return (- 1)
    logging.info('Starting TensorBoard in directory %s', os.getcwd())
    path_to_run = server.ParseEventFilesSpec(logdir)
    logging.info('TensorBoard path_to_run is: %s', path_to_run)
    multiplexer = event_multiplexer.EventMultiplexer(size_guidance=server.TENSORBOARD_SIZE_GUIDANCE, purge_orphaned_data=FLAGS.purge_orphaned_data)
    server.StartMultiplexerReloadingThread(multiplexer, path_to_run, FLAGS.reload_interval)
    try:
        tb_server = server.BuildServer(multiplexer, FLAGS.host, FLAGS.port)
    except socket.error:
        if (FLAGS.port == 0):
            msg = 'Unable to find any open ports.'
            logging.error(msg)
            print(msg)
            return (- 2)
        else:
            msg = ('Tried to connect to port %d, but address is in use.' % FLAGS.port)
            logging.error(msg)
            print(msg)
            return (- 3)
    try:
        tag = resource_loader.load_resource('tensorboard/TAG').strip()
        logging.info('TensorBoard is tag: %s', tag)
    except IOError:
        logging.info('Unable to read TensorBoard tag')
        tag = ''
    status_bar.SetupStatusBarInsideGoogle(('TensorBoard %s' % tag), FLAGS.port)
    print(('Starting TensorBoard %s on port %d' % (tag, FLAGS.port)))
    if (FLAGS.host == '0.0.0.0'):
        print(('(You can navigate to http://%s:%d)' % (socket.gethostbyname(socket.gethostname()), FLAGS.port)))
    else:
        print(('(You can navigate to http://%s:%d)' % (FLAGS.host, FLAGS.port)))
    tb_server.serve_forever()
