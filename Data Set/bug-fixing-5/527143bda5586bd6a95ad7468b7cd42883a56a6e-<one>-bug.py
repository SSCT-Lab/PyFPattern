@pytest.fixture(params=[1, np.array(1, dtype=np.int64)])
def one(request):
    return request.param