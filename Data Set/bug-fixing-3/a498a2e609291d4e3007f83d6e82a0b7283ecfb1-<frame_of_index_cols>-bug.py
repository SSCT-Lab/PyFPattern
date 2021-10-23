@pytest.fixture
def frame_of_index_cols():
    "\n    Fixture for DataFrame of columns that can be used for indexing\n\n    Columns are ['A', 'B', 'C', 'D', 'E', ('tuple', 'as', 'label')];\n    'A' & 'B' contain duplicates (but are jointly unique), the rest are unique.\n    "
    df = DataFrame({
        'A': ['foo', 'foo', 'foo', 'bar', 'bar'],
        'B': ['one', 'two', 'three', 'one', 'two'],
        'C': ['a', 'b', 'c', 'd', 'e'],
        'D': np.random.randn(5),
        'E': np.random.randn(5),
        ('tuple', 'as', 'label'): np.random.randn(5),
    })
    return df