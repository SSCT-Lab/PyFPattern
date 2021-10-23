def getRuleStringForVariable(deviceType, ruleFile, variableId):
    retVal = ''
    try:
        f = open(errorFile, 'r')
        for line in f:
            if (':' in line):
                data = line.split(':')
                if (data[0].strip() == variableId):
                    retVal = line
    except Exception:
        ruleString = cnos_devicerules.getRuleString(deviceType, variableId)
        retVal = ruleString.strip()
    return retVal