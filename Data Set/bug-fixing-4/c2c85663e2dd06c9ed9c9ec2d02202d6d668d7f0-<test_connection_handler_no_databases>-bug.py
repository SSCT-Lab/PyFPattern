def test_connection_handler_no_databases(self):
    'Empty DATABASES setting defaults to the dummy backend.'
    DATABASES = {
        
    }
    conns = ConnectionHandler(DATABASES)
    self.assertEqual(conns[DEFAULT_DB_ALIAS].settings_dict['ENGINE'], 'django.db.backends.dummy')
    msg = 'settings.DATABASES is improperly configured. Please supply the ENGINE value. Check settings documentation for more details.'
    with self.assertRaisesMessage(ImproperlyConfigured, msg):
        conns[DEFAULT_DB_ALIAS].ensure_connection()