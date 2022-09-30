import pigpio
import time


def readmessage(message):
    message = message[ : len(message) - 9]
    #print(message)
    resultstring = ""
    for i in range(int(len(message)/9)):
        char = message[i*9:(i*9)+8]
        #print(char)
        char = "0b" + char
        resultnum = int(char, 2)
        resultchar = chr(resultnum)
        resultstring = resultstring + resultchar
    return resultstring    


def receive():

    pi = pigpio.pi()
    timedelay = 0.002
    pi.set_mode(26, pigpio.INPUT)
    bitstring = ""
    latestbit = "0"
    isMessage = False

    while (True) :
        clear = pi.read(26)
        if(clear == 0):
            #print("Clear: " + str(clear))
            break

    while (True) :
        read = pi.read(26)
        if (read != int(latestbit)) :
            #print("Indicator: " + str(read))
            time.sleep(timedelay)
            latestbit = str(pi.read(26))
            #print("Value: " + latestbit)
            bitstring = bitstring + latestbit
            if (len(bitstring) >= 9):
                closer = bitstring[len(bitstring) - 9 : ]
                #print(closer)
                if (closer == "100000000"):
                    message = readmessage(bitstring)
                    print("RCV: " + message)
                    bitstring = ""

