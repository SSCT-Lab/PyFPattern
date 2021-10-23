@pytest.fixture(params=zeros)
def zero(request):
    "\n    Several types of scalar zeros and length 5 vectors of zeros.\n\n    This fixture can be used to check that numeric-dtype indexes handle\n    division by any zero numeric-dtype.\n\n    Uses vector of length 5 for broadcasting with `numeric_idx` fixture,\n    which creates numeric-dtype vectors also of length 5.\n\n    Examples\n    --------\n    >>> arr = pd.RangeIndex(5)\n    >>> arr / zeros\n    Float64Index([nan, inf, inf, inf, inf], dtype='float64')\n    "
    return request.param