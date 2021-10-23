@pytest.fixture(params=zeros)
def zero(request):
    return request.param