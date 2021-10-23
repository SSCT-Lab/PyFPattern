def backend_pyqt4_internal_check(self):
    try:
        from PyQt4 import QtCore
    except ImportError:
        raise CheckFailed('PyQt4 not found')
    try:
        qt_version = QtCore.QT_VERSION
        pyqt_version_str = QtCore.PYQT_VERSION_STR
    except AttributeError:
        raise CheckFailed('PyQt4 not correctly imported')
    else:
        return ('Qt: %s, PyQt: %s' % (self.convert_qt_version(qt_version), pyqt_version_str))