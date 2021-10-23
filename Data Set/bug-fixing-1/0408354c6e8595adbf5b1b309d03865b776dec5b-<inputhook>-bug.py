

def inputhook(context):
    global _appref
    app = QtCore.QCoreApplication.instance()
    if (not app):
        _appref = app = QtGui.QApplication([' '])
    event_loop = QtCore.QEventLoop(app)
    if (sys.platform == 'win32'):
        timer = QtCore.QTimer()
        timer.timeout.connect(event_loop.quit)
        while (not context.input_is_ready()):
            timer.start(50)
            event_loop.exec_()
            timer.stop()
    else:
        notifier = QtCore.QSocketNotifier(context.fileno(), QtCore.QSocketNotifier.Read)
        notifier.setEnabled(True)
        notifier.activated.connect(event_loop.exit)
        event_loop.exec_()
