

@skipUnlessDBFeature('has_select_for_update')
@skipUnlessDBFeature('supports_transactions')
def test_block(self):
    '\n        A thread running a select_for_update that accesses rows being touched\n        by a similar operation on another connection blocks correctly.\n        '
    self.start_blocking_transaction()
    status = []
    thread = threading.Thread(target=self.run_select_for_update, args=(status,))
    thread.start()
    sanity_count = 0
    while ((len(status) != 1) and (sanity_count < 10)):
        sanity_count += 1
        time.sleep(1)
    if (sanity_count >= 10):
        raise ValueError('Thread did not run and block')
    p = Person.objects.get(pk=self.person.pk)
    self.assertEqual('Reinhardt', p.name)
    self.end_blocking_transaction()
    thread.join(5.0)
    self.assertFalse(thread.isAlive())
    transaction.commit()
    p = Person.objects.get(pk=self.person.pk)
    self.assertEqual('Fred', p.name)
