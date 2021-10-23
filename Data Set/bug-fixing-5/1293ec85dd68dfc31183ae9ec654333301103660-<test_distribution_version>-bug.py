def test_distribution_version():
    'tests the distribution parsing code of the Facts class\n\n    testsets have\n    * a name (for output/debugging only)\n    * input files that are faked\n      * those should be complete and also include "irrelevant" files that might be mistaken as coming from other distributions\n      * all files that are not listed here are assumed to not exist at all\n    * the output of pythons platform.dist()\n    * results for the ansible variables distribution* and os_family\n    '
    from ansible.module_utils import basic
    args = json.dumps(dict(ANSIBLE_MODULE_ARGS={
        
    }))
    with swap_stdin_and_argv(stdin_data=args):
        basic._ANSIBLE_ARGS = None
        module = basic.AnsibleModule(argument_spec=dict())
        for t in TESTSETS:
            _test_one_distribution.description = ('check distribution_version for %s' % t['name'])
            (yield (_test_one_distribution, facts, module, t))