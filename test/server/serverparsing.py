def appendOutData(data, append):
    data += append
    return data

def capOutData(data, cap):
    outDataIndexZero = getOutDataIndex(data)
    print(outDataIndexZero)
    data = data[:outDataIndexZero + 1] + data[outDataIndexZero + 1 + cap:]
    return data

def getOutDataIndex(data):
    outDataIndexZero = 0
    for i in range(len(data)):
        outDataIndexZero = i
        if data[i] == 0x7C:
            break
        if i == len(data) - 1:
            print("Data not properly formatted, outDataIndex could not be found")
    return outDataIndexZero

def getPortIndex(data):
    portIndex = 0
    for i in range(len(data)):
        portIndex = i
        if data[i] == 0x3A:
            break
        if i == len(data) - 1:
            print("Data not properly formatted, portIndex could not be found")
    return portIndex

def getAddrIndex(data):
    addrIndex = 0
    for i in range(len(data)):
        addrIndex = i
        if data[i] == 0x3B:
            break
        if i == len(data) - 1:
            print("Data not properly formatted, addrIndex could not be found")
    return addrIndex

def getRequestData(data):
    return data[:getAddrIndex(data)]

def getAddr(data):
    return data[getAddrIndex(data)+1:getPortIndex(data)]

def getPort(data):
    return data[getPortIndex(data)+1:getOutDataIndex(data)]

def getOutData(data):
    return data[getOutDataIndex(data)+1:]

def capOutData(data, cap):
    outDataIndexZero = getOutDataIndex(data)
    data = data[:outDataIndexZero + 1] + data[outDataIndexZero + 1 + cap:]
    return data

dat = b'runNetwork;127.0.0.1:5656|Hej varld osv'

dat = capOutData(dat, 13)