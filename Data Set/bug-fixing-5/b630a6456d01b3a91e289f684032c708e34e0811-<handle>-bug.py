def handle(self, *args: Any, **options: str) -> None:
    values = query_ldap(**options)
    for value in values:
        print(value)