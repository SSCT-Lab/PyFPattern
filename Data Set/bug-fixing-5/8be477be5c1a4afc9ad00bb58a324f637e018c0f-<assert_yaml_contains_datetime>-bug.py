def assert_yaml_contains_datetime(self, yaml, dt):
    self.assertRegex(yaml, ("\\n  fields: {dt: !(!timestamp)? '%s'}" % re.escape(dt)))