def test(self, args, targets):
    '\n        :type args: SanityConfig\n        :type targets: SanityTargets\n        :rtype: TestResult\n        '
    if args.explain:
        return SanitySuccess(self.name)
    if (not os.path.isfile(self.SHIPPABLE_YML)):
        return SanityFailure(self.name, messages=[SanityMessage(message='file missing', path=self.SHIPPABLE_YML)])
    results = dict(comments=[], labels={
        
    })
    self.check_changes(args, results)
    with open('test/results/bot/data-sanity-ci.json', 'w') as results_fd:
        json.dump(results, results_fd, sort_keys=True, indent=4)
    messages = []
    messages += self.check_posix_targets(args)
    messages += self.check_windows_targets()
    if messages:
        return SanityFailure(self.name, messages=messages)
    return SanitySuccess(self.name)