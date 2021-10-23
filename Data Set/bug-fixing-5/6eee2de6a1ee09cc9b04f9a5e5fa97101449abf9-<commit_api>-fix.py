def commit_api(api):
    'Commit to a particular API, and trigger ImportErrors on subsequent\n       dangerous imports'
    if (api == QT_API_PYSIDE2):
        ID.forbid('PySide')
        ID.forbid('PyQt4')
        ID.forbid('PyQt5')
    elif (api == QT_API_PYSIDE):
        ID.forbid('PySide2')
        ID.forbid('PyQt4')
        ID.forbid('PyQt5')
    elif (api == QT_API_PYQT5):
        ID.forbid('PySide2')
        ID.forbid('PySide')
        ID.forbid('PyQt4')
    else:
        ID.forbid('PyQt5')
        ID.forbid('PySide2')
        ID.forbid('PySide')