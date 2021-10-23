@unittest.skipUnless((tblib is not None), 'requires tblib to be installed')
def test_add_failing_subtests(self):
    '\n        Failing subtests are added correctly using addSubTest().\n        '
    result = RemoteTestResult()
    subtest_test = SampleFailingSubtest(methodName='dummy_test')
    subtest_test.run(result=result)
    events = result.events
    self.assertEqual(len(events), 4)
    event = events[1]
    self.assertEqual(event[0], 'addSubTest')
    self.assertEqual(str(event[2]), 'dummy_test (test_runner.test_parallel.SampleFailingSubtest) (index=0)')
    trailing_comma = ('' if PY37 else ',')
    self.assertEqual(repr(event[3][1]), ("AssertionError('0 != 1'%s)" % trailing_comma))
    event = events[2]
    self.assertEqual(repr(event[3][1]), ("AssertionError('2 != 1'%s)" % trailing_comma))