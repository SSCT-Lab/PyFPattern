@pytest.fixture
def frame_of_index_cols():
    "\n    Fixture for DataFrame of columns that can be used for indexing\n\n    Columns are ['A', 'B', 'C', 'D', 'E', ('tuple', 'as', 'label')];\n    'A' & 'B' contain duplicates (but are jointly unique), the rest are unique.\n\n         A      B  C         D         E  (tuple, as, label)\n    0  foo    one  a  0.608477 -0.012500           -1.664297\n    1  foo    two  b -0.633460  0.249614           -0.364411\n    2  foo  three  c  0.615256  2.154968           -0.834666\n    3  bar    one  d  0.234246  1.085675            0.718445\n    4  bar    two  e  0.533841 -0.005702           -3.533912\n    "
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar'],
        'B': ['one', 'two', 'three', 'one', 'two'],
        'C': ['a', 'b', 'c', 'd', 'e'],
        'D': np.random.randn(5),
        'E': np.random.randn(5),
        ('tuple', 'as', 'label'): np.random.randn(5),
    })
    return df