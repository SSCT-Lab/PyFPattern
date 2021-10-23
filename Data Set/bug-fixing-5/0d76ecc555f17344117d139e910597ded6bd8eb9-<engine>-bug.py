@pytest.fixture(params=[pytest.param('xlrd', marks=[td.skip_if_no('xlrd'), pytest.mark.filterwarnings('ignore:.*(tree\\.iter|html argument)')]), pytest.param('openpyxl', marks=[td.skip_if_no('openpyxl'), pytest.mark.filterwarnings('ignore:.*html argument')]), pytest.param(None, marks=[td.skip_if_no('xlrd'), pytest.mark.filterwarnings('ignore:.*(tree\\.iter|html argument)')]), pytest.param('odf', marks=td.skip_if_no('odf'))])
def engine(request):
    '\n    A fixture for Excel reader engines.\n    '
    return request.param