def test_connection_handler_no_databases(self):
    "\n        Empty DATABASES and empty 'default' settings default to the dummy\n        backend.\n        "
    for DATABASES in ({
        
    }, {
        'default': {
            
        },
    }):
        with self.subTest(DATABASES=DATABASES):
            self.assertImproperlyConfigured(DATABASES)