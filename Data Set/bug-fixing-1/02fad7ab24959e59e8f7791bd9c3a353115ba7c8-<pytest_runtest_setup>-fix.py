

def pytest_runtest_setup(item):
    fname = item.fspath.strpath
    is_index = fname.endswith('datasets/index.rst')
    if (fname.endswith('datasets/labeled_faces.rst') or is_index):
        setup_labeled_faces()
    elif (fname.endswith('datasets/mldata.rst') or is_index):
        setup_mldata()
    elif (fname.endswith('datasets/rcv1.rst') or is_index):
        setup_rcv1()
    elif (fname.endswith('datasets/twenty_newsgroups.rst') or is_index):
        setup_twenty_newsgroups()
    elif (fname.endswith('tutorial/text_analytics/working_with_text_data.rst') or is_index):
        setup_working_with_text_data()
    elif (fname.endswith('modules/compose.rst') or is_index):
        setup_compose()
