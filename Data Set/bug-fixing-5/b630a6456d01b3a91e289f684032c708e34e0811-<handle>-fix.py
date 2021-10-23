def handle(self, *args: Any, **options: str) -> None:
    email = options['email']
    values = query_ldap(email)
    for value in values:
        print(value)