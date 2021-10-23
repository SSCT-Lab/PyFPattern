

def validateValueAgainstRule(ruleString, variableValue):
    retVal = ''
    if (ruleString == ''):
        return 1
    rules = ruleString.split(':')
    variableType = rules[1].strip()
    varRange = rules[2].strip()
    if (variableType == 'INTEGER'):
        result = checkInteger(variableValue)
        if (result is True):
            return 'ok'
        else:
            return 'Error-111'
    elif (variableType == 'FLOAT'):
        result = checkFloat(variableValue)
        if (result is True):
            return 'ok'
        else:
            return 'Error-112'
    elif (variableType == 'INTEGER_VALUE'):
        int_range = varRange.split('-')
        r = range(int(int_range[0].strip()), int(int_range[1].strip()))
        if (checkInteger(variableValue) is not True):
            return 'Error-111'
        result = (int(variableValue) in r)
        if (result is True):
            return 'ok'
        else:
            return 'Error-113'
    elif (variableType == 'INTEGER_VALUE_RANGE'):
        int_range = varRange.split('-')
        varLower = int_range[0].strip()
        varHigher = int_range[1].strip()
        r = range(int(varLower), int(varHigher))
        val_range = variableValue.split('-')
        try:
            valLower = val_range[0].strip()
            valHigher = val_range[1].strip()
        except Exception:
            return 'Error-113'
        if ((checkInteger(valLower) is not True) or (checkInteger(valHigher) is not True)):
            return 'Error-114'
        result = ((int(valLower) in r) and (int(valHigher) in r) and (int(valLower) < int(valHigher)))
        if (result is True):
            return 'ok'
        else:
            return 'Error-113'
    elif (variableType == 'INTEGER_OPTIONS'):
        int_options = varRange.split(',')
        if (checkInteger(variableValue) is not True):
            return 'Error-111'
        for opt in int_options:
            if (opt.strip() is variableValue):
                result = True
                break
        if (result is True):
            return 'ok'
        else:
            return 'Error-115'
    elif (variableType == 'LONG'):
        result = checkLong(variableValue)
        if (result is True):
            return 'ok'
        else:
            return 'Error-116'
    elif (variableType == 'LONG_VALUE'):
        long_range = varRange.split('-')
        r = range(int(long_range[0].strip()), int(long_range[1].strip()))
        if (checkLong(variableValue) is not True):
            return 'Error-116'
        result = (int(variableValue) in r)
        if (result is True):
            return 'ok'
        else:
            return 'Error-113'
    elif (variableType == 'LONG_VALUE_RANGE'):
        long_range = varRange.split('-')
        r = range(int(long_range[0].strip()), int(long_range[1].strip()))
        val_range = variableValue.split('-')
        if ((checkLong(val_range[0]) is not True) or (checkLong(val_range[1]) is not True)):
            return 'Error-117'
        result = ((val_range[0] in r) and (val_range[1] in r) and (val_range[0] < val_range[1]))
        if (result is True):
            return 'ok'
        else:
            return 'Error-113'
    elif (variableType == 'LONG_OPTIONS'):
        long_options = varRange.split(',')
        if (checkLong(variableValue) is not True):
            return 'Error-116'
        for opt in long_options:
            if (opt.strip() == variableValue):
                result = True
                break
        if (result is True):
            return 'ok'
        else:
            return 'Error-115'
    elif (variableType == 'TEXT'):
        if (variableValue == ''):
            return 'Error-118'
        if (True is isinstance(variableValue, str)):
            return 'ok'
        else:
            return 'Error-119'
    elif (variableType == 'NO_VALIDATION'):
        if (variableValue == ''):
            return 'Error-118'
        else:
            return 'ok'
    elif (variableType == 'TEXT_OR_EMPTY'):
        if ((variableValue is None) or (variableValue == '')):
            return 'ok'
        if (result == isinstance(variableValue, str)):
            return 'ok'
        else:
            return 'Error-119'
    elif (variableType == 'MATCH_TEXT'):
        if (variableValue == ''):
            return 'Error-118'
        if isinstance(variableValue, str):
            if (varRange == variableValue):
                return 'ok'
            else:
                return 'Error-120'
        else:
            return 'Error-119'
    elif (variableType == 'MATCH_TEXT_OR_EMPTY'):
        if ((variableValue is None) or (variableValue == '')):
            return 'ok'
        if isinstance(variableValue, str):
            if (varRange == variableValue):
                return 'ok'
            else:
                return 'Error-120'
        else:
            return 'Error-119'
    elif (variableType == 'TEXT_OPTIONS'):
        str_options = varRange.split(',')
        if (isinstance(variableValue, str) is not True):
            return 'Error-119'
        result = False
        for opt in str_options:
            if (opt.strip() == variableValue):
                result = True
                break
        if (result is True):
            return 'ok'
        else:
            return 'Error-115'
    elif (variableType == 'TEXT_OPTIONS_OR_EMPTY'):
        if ((variableValue is None) or (variableValue == '')):
            return 'ok'
        str_options = varRange.split(',')
        if (isinstance(variableValue, str) is not True):
            return 'Error-119'
        for opt in str_options:
            if (opt.strip() == variableValue):
                result = True
                break
        if (result is True):
            return 'ok'
        else:
            return 'Error-115'
    elif (variableType == 'IPV4Address'):
        try:
            socket.inet_pton(socket.AF_INET, variableValue)
            result = True
        except socket.error:
            result = False
        if (result is True):
            return 'ok'
        else:
            return 'Error-121'
    elif (variableType == 'IPV4AddressWithMask'):
        if ((variableValue is None) or (variableValue == '')):
            return 'Error-119'
        str_options = variableValue.split('/')
        ipaddr = str_options[0]
        mask = str_options[1]
        try:
            socket.inet_pton(socket.AF_INET, ipaddr)
            if (checkInteger(mask) is True):
                result = True
            else:
                result = False
        except socket.error:
            result = False
        if (result is True):
            return 'ok'
        else:
            return 'Error-121'
    elif (variableType == 'IPV6Address'):
        try:
            socket.inet_pton(socket.AF_INET6, variableValue)
            result = True
        except socket.error:
            result = False
        if (result is True):
            return 'ok'
        else:
            return 'Error-122'
    return retVal
