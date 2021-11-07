def appendOutData(data, append):
    data += append
    return data

# Removes pieces of the output data in order to not send duplicates (all data is not always sent i a single cycle)
def capOutData(data, cap):
    outDataIndexZero = getOutDataIndex(data)
    data = data[:outDataIndexZero + 1] + data[outDataIndexZero + 1 + cap:]
    return data

def getOutDataIndex(data):
    outDataIndexZero = 0
    for i in range(len(data)):
        outDataIndexZero = i
        if data[i] == 0x7C:
            return outDataIndexZero
    print("Data not properly formatted, outDataIndex could not be found")
    return None

def getPortIndex(data):
    portIndex = 0
    for i in range(len(data)):
        portIndex = i
        if data[i] == 0x3A:
            return portIndex
    print("Data not properly formatted, portIndex could not be found")
    return None

def getAddrIndex(data):
    return 0

def getRequestIndex(data):
    dataIndex = 0
    for i in range(len(data)):
        dataIndex = i
        if data[i] == 0x3B: # semicolon
            return dataIndex
    print("Data not properly formatted, dataIndex could not be found")
    return None
# ADDR:PORT;REQUEST|INPUT
def getAddr(data):
    print(data)
    return data[getAddrIndex(data):getPortIndex(data)]

def getRequest(data):
    return data[getRequestIndex(data)+1:getOutDataIndex(data)]

def getPort(data):
    return data[getPortIndex(data)+1:getRequestIndex(data)]

def getOutData(data):
    return data[getOutDataIndex(data)+1:]

addr = ["127.0.0.1", 5656]
data = str(addr[0]).encode("UTF-8") + b':' + str(addr[1]).encode("UTF-8") + b';'
data += b'runNetwork' + b'|' + b'Hej varld osv'

print(data)
print(getOutData(data))