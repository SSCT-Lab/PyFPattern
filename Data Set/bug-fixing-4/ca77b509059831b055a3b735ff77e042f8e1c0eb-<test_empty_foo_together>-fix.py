def test_empty_foo_together(self):
    "\n        #23452 - Empty unique/index_together shouldn't generate a migration.\n        "
    model_state_not_specified = ModelState('a', 'model', [('id', models.AutoField(primary_key=True))])
    model_state_none = ModelState('a', 'model', [('id', models.AutoField(primary_key=True))], {
        'index_together': None,
        'unique_together': None,
    })
    model_state_empty = ModelState('a', 'model', [('id', models.AutoField(primary_key=True))], {
        'index_together': set(),
        'unique_together': set(),
    })

    def test(from_state, to_state, msg):
        changes = self.get_changes([from_state], [to_state])
        if (len(changes) > 0):
            ops = ', '.join((o.__class__.__name__ for o in changes['a'][0].operations))
            self.fail(('Created operation(s) %s from %s' % (ops, msg)))
    tests = ((model_state_not_specified, model_state_not_specified, '"not specified" to "not specified"'), (model_state_not_specified, model_state_none, '"not specified" to "None"'), (model_state_not_specified, model_state_empty, '"not specified" to "empty"'), (model_state_none, model_state_not_specified, '"None" to "not specified"'), (model_state_none, model_state_none, '"None" to "None"'), (model_state_none, model_state_empty, '"None" to "empty"'), (model_state_empty, model_state_not_specified, '"empty" to "not specified"'), (model_state_empty, model_state_none, '"empty" to "None"'), (model_state_empty, model_state_empty, '"empty" to "empty"'))
    for t in tests:
        test(*t)