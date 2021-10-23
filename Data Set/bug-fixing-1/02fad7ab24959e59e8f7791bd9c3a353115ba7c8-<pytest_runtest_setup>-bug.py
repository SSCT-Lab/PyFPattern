

def pytest_runtest_setup(item):
    fname = item.fspath.strpath
    if fname.endswith('datasets/labeled_faces.rst'):
        setup_labeled_faces()
    elif fname.endswith('datasets/mldata.rst'):
        setup_mldata()
    elif fname.endswith('datasets/rcv1.rst'):
        setup_rcv1()
    elif fname.endswith('datasets/twenty_newsgroups.rst'):
        setup_twenty_newsgroups()
    elif fname.endswith('tutorial/text_analytics/working_with_text_data.rst'):
        setup_working_with_text_data()
    elif fname.endswith('modules/compose.rst'):
        setup_compose()
