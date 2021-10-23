@skipUnlessDBFeature('has_select_for_update')
@skipUnlessDBFeature('supports_transactions')
def test_updates_in_transaction(self):
    "\n        Objects are selected and updated in a transaction to avoid race\n        conditions. This test forces update_or_create() to hold the lock\n        in another thread for a relatively long time so that it can update\n        while it holds the lock. The updated field isn't a field in 'defaults',\n        so update_or_create() shouldn't have an effect on it.\n        "
    lock_status = {
        'has_grabbed_lock': False,
    }

    def birthday_sleep():
        lock_status['has_grabbed_lock'] = True
        time.sleep(0.5)
        return date(1940, 10, 10)

    def update_birthday_slowly():
        Person.objects.update_or_create(first_name='John', defaults={
            'birthday': birthday_sleep,
        })
        connection.close()

    def lock_wait():
        for i in range(20):
            time.sleep(0.025)
            if lock_status['has_grabbed_lock']:
                return True
        return False
    Person.objects.create(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
    t = Thread(target=update_birthday_slowly)
    before_start = datetime.now()
    t.start()
    if (not lock_wait()):
        self.skipTest('Database took too long to lock the row')
    Person.objects.filter(first_name='John').update(last_name='NotLennon')
    after_update = datetime.now()
    t.join()
    updated_person = Person.objects.get(first_name='John')
    self.assertGreater((after_update - before_start), timedelta(seconds=0.5))
    self.assertEqual(updated_person.last_name, 'NotLennon')