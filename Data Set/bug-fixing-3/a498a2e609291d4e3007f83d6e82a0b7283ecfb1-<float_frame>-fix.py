@pytest.fixture
def float_frame():
    "\n    Fixture for DataFrame of floats with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n\n                       A         B         C         D\n    P7GACiRnxd -0.465578 -0.361863  0.886172 -0.053465\n    qZKh6afn8n -0.466693 -0.373773  0.266873  1.673901\n    tkp0r6Qble  0.148691 -0.059051  0.174817  1.598433\n    wP70WOCtv8  0.133045 -0.581994 -0.992240  0.261651\n    M2AeYQMnCz -1.207959 -0.185775  0.588206  0.563938\n    QEPzyGDYDo -0.381843 -0.758281  0.502575 -0.565053\n    r78Jwns6dn -0.653707  0.883127  0.682199  0.206159\n    ...              ...       ...       ...       ...\n    IHEGx9NO0T -0.277360  0.113021 -1.018314  0.196316\n    lPMj8K27FA -1.313667 -0.604776 -1.305618 -0.863999\n    qa66YMWQa5  1.110525  0.475310 -0.747865  0.032121\n    yOa0ATsmcE -0.431457  0.067094  0.096567 -0.264962\n    65znX3uRNG  1.528446  0.160416 -0.109635 -0.032987\n    eCOBvKqf3e  0.235281  1.622222  0.781255  0.392871\n    xSucinXxuV -1.263557  0.252799 -0.552247  0.400426\n\n    [30 rows x 4 columns]\n    "
    return DataFrame(tm.getSeriesData())