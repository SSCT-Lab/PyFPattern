def assertOptimizesTo(self, operations, expected, exact=None, less_than=None, app_label=None):
    (result, iterations) = self.optimize(operations, app_label)
    result = [self.serialize(f) for f in result]
    expected = [self.serialize(f) for f in expected]
    self.assertEqual(expected, result)
    if ((exact is not None) and (iterations != exact)):
        raise self.failureException(('Optimization did not take exactly %s iterations (it took %s)' % (exact, iterations)))
    if ((less_than is not None) and (iterations >= less_than)):
        raise self.failureException(('Optimization did not take less than %s iterations (it took %s)' % (less_than, iterations)))