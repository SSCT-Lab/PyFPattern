def privileges_get(cursor, user, host):
    " MySQL doesn't have a better method of getting privileges aside from the\n    SHOW GRANTS query syntax, which requires us to then parse the returned string.\n    Here's an example of the string that is returned from MySQL:\n\n     GRANT USAGE ON *.* TO 'user'@'localhost' IDENTIFIED BY 'pass';\n\n    This function makes the query and returns a dictionary containing the results.\n    The dictionary format is the same as that returned by privileges_unpack() below.\n    "
    output = {
        
    }
    cursor.execute('SHOW GRANTS FOR %s@%s', (user, host))
    grants = cursor.fetchall()

    def pick(x):
        if (x == 'ALL PRIVILEGES'):
            return 'ALL'
        else:
            return x
    for grant in grants:
        res = re.match("GRANT (.+) ON (.+) TO '.*'@'.*'( IDENTIFIED BY PASSWORD '.+')? ?(.*)", grant[0])
        if (res is None):
            raise InvalidPrivsError(('unable to parse the MySQL grant string: %s' % grant[0]))
        privileges = res.group(1).split(', ')
        privileges = [pick(x) for x in privileges]
        if ('WITH GRANT OPTION' in res.group(4)):
            privileges.append('GRANT')
        if ('REQUIRE SSL' in res.group(4)):
            privileges.append('REQUIRESSL')
        db = res.group(2)
        output[db] = privileges
    return output