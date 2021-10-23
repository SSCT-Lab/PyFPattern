def checkOutputForError(output):
    retVal = ''
    index = output.lower().find('error')
    startIndex = (index + 6)
    if (index == (- 1)):
        index = output.lower().find('invalid')
        startIndex = (index + 8)
        if (index == (- 1)):
            index = output.lower().find('cannot be enabled in l2 interface')
            startIndex = (index + 34)
            if (index == (- 1)):
                index = output.lower().find('incorrect')
                startIndex = (index + 10)
                if (index == (- 1)):
                    index = output.lower().find('failure')
                    startIndex = (index + 8)
                    if (index == (- 1)):
                        return None
    endIndex = (startIndex + 3)
    errorCode = output[startIndex:endIndex]
    result = errorCode.isdigit()
    if (result is not True):
        return 'Device returned an Error. Please check Results for more         information'
    errorFile = 'dictionary/ErrorCodes.lvo'
    try:
        f = open(errorFile, 'r')
        for line in f:
            if ('=' in line):
                data = line.split('=')
                if (data[0].strip() == errorCode):
                    errorString = data[1].strip()
                    return errorString
    except Exception:
        errorString = cnos_errorcodes.getErrorString(errorCode)
        errorString = errorString.strip()
        return errorString
    return 'Error Code Not Found'