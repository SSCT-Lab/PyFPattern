def waitForDeviceResponse(command, prompt, timeout, obj):
    obj.settimeout(int(timeout))
    obj.send(command)
    flag = False
    retVal = ''
    while (not flag):
        time.sleep(1)
        try:
            buffByte = obj.recv(9999)
            buff = buffByte.decode()
            retVal = (retVal + buff)
            gotit = buff.find(prompt)
            if (gotit != (- 1)):
                flag = True
        except:
            if (prompt == '(yes/no)?'):
                retVal = retVal
            elif (prompt == 'Password:'):
                retVal = retVal
            else:
                retVal = (retVal + '\n Error-101')
            flag = True
    return retVal