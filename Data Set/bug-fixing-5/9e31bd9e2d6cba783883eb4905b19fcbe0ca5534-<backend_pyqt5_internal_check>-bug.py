def backend_pyqt5_internal_check(self):
    try:
        from PyQt5 import QtCore
    except ImportError:
        raise CheckFailed('PyQt5 not found')
    try:
        qt_version = QtCore.QT_VERSION
        pyqt_version_str = QtCore.QT_VERSION_STR
    except AttributeError:
        raise CheckFailed('PyQt5 not correctly imported')
    else:
        return ('Qt: %s, PyQt: %s' % (self.convert_qt_version(qt_version), pyqt_version_str))