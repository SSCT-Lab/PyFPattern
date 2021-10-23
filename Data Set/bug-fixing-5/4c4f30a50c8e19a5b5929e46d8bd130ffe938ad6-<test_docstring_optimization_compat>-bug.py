@pytest.mark.skipif(SCIPY_11, reason='SciPy raises on -OO')
def test_docstring_optimization_compat():
    p = subprocess.Popen('python -OO -c "import statsmodels.api as sm"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.communicate()
    rc = p.returncode
    assert (rc == 0), out