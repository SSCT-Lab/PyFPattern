def test_to_string_unicode_columns(self):
    df = DataFrame({
        'σ': np.arange(10.0),
    })
    buf = StringIO()
    df.to_string(buf=buf)
    buf.getvalue()
    buf = StringIO()
    df.info(buf=buf)
    buf.getvalue()
    result = self.frame.to_string()
    assert isinstance(result, str)