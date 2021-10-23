@skipUnlessDBFeature('has_select_for_update')
@skipUnlessDBFeature('supports_transactions')
def test_updates_in_transaction(self):
    "\n        Objects are selected and updated in a transaction to avoid race\n        conditions. This test forces update_or_create() to hold the lock\n        in another thread for a relatively long time so that it can update\n        while it holds the lock. The updated field isn't a field in 'defaults',\n        so update_or_create() shouldn't have an effect on it.\n        "

    def birthday_sleep():
        time.sleep(0.3)
        return date(1940, 10, 10)

    def update_birthday_slowly():
        Person.objects.update_or_create(first_name='John', defaults={
            'birthday': birthday_sleep,
        })
    Person.objects.create(first_name='John', last_name='Lennon', birthday=date(1940, 10, 9))
    t = Thread(target=update_birthday_slowly)
    before_start = datetime.now()
    t.start()
    time.sleep(0.05)
    Person.objects.filter(first_name='John').update(last_name='NotLennon')
    after_update = datetime.now()
    t.join()
    updated_person = Person.objects.get(first_name='John')
    self.assertGreater((after_update - before_start), timedelta(seconds=0.3))
    self.assertEqual(updated_person.last_name, 'NotLennon')