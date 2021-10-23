@pytest.fixture
def simple_frame():
    "\n    Fixture for simple 3x3 DataFrame\n\n    Columns are ['one', 'two', 'three'], index is ['a', 'b', 'c'].\n\n       one  two  three\n    a  1.0  2.0    3.0\n    b  4.0  5.0    6.0\n    c  7.0  8.0    9.0\n    "
    arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
    return DataFrame(arr, columns=['one', 'two', 'three'], index=['a', 'b', 'c'])