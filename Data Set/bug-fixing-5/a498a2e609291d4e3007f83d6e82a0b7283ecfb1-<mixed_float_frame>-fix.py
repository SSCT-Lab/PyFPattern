@pytest.fixture
def mixed_float_frame():
    "\n    Fixture for DataFrame of different float types with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n\n                       A         B         C         D\n    GI7bbDaEZe -0.237908 -0.246225 -0.468506  0.752993\n    KGp9mFepzA -1.140809 -0.644046 -1.225586  0.801588\n    VeVYLAb1l2 -1.154013 -1.677615  0.690430 -0.003731\n    kmPME4WKhO  0.979578  0.998274 -0.776367  0.897607\n    CPyopdXTiz  0.048119 -0.257174  0.836426  0.111266\n    0kJZQndAj0  0.274357 -0.281135 -0.344238  0.834541\n    tqdwQsaHG8 -0.979716 -0.519897  0.582031  0.144710\n    ...              ...       ...       ...       ...\n    7FhZTWILQj -2.906357  1.261039 -0.780273 -0.537237\n    4pUDPM4eGq -2.042512 -0.464382 -0.382080  1.132612\n    B8dUgUzwTi -1.506637 -0.364435  1.087891  0.297653\n    hErlVYjVv9  1.477453 -0.495515 -0.713867  1.438427\n    1BKN3o7YLs  0.127535 -0.349812 -0.881836  0.489827\n    9S4Ekn7zga  1.445518 -2.095149  0.031982  0.373204\n    xN1dNn6OV6  1.425017 -0.983995 -0.363281 -0.224502\n\n    [30 rows x 4 columns]\n    "
    df = DataFrame(tm.getSeriesData())
    df.A = df.A.astype('float32')
    df.B = df.B.astype('float32')
    df.C = df.C.astype('float16')
    df.D = df.D.astype('float64')
    return df