import os
import time
import serial

# import serial.tools.list_ports
# ports = serial.tools.list_ports.comports()


def printPortInfo():
    # for port, desc, hwid in sorted(ports):
    #     print("{}: \t{} \t[{}]".format(port, desc, hwid))
    os.system('python -m serial.tools.list_ports -v')


def openPort(port, baudRate=9600):
    return serial.Serial(port, baudRate)


def closePort(serialPort):
    serialPort.close()


def sendLayerType(ser, layerType):
    packet = bytearray()
    packet.append(layerType)
    ser.write(packet)


def sendShape(ser, M, C, P, Q, R, S, xStride, yStride):
    packet = bytearray([M, C, P, Q, R, S, xStride, yStride])
    ser.write(packet)


def sendInput(ser, csvFile):
    values = range(32)
    packet = bytearray()
    for _ in values:
        packet.append(2)

    ser.write(packet)


def sendWeight(ser, csvFile):
    values = range(16)
    packet = bytearray()
    for _ in values:
        packet.append(csvFile)

    ser.write(packet)


def readOutput(ser, M, C, P, Q, R, S, xStride, yStride):
    size = M*P*Q
    values = range(size)
    packet = bytearray()

    for _ in values:
        x = ser.read()
        valx = int.from_bytes(x, "big")
        print(valx)
        packet.append(valx)

    print("Printing from DS")
    for i in packet:
        print(i)


# some testing example
# def sendShapeTest(M,C,P,Q,R,S,xStride,yStride):
#     ser = serial.Serial(port,baudRate)
#     packet = bytearray()
#     packet.append(M)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(C)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(P)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(Q)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(R)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(S)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(xStride)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     packet.append(yStride)
#     ser.write(packet)
#     packet = bytearray()
#     time.sleep(1)

#     ser.close()

# print(list(serial.tools.list_ports.comports()))

# sendShape(2,2,3,3,2,2,1,1)


def main():
    printPortInfo()
    myPort = openPort(port="/dev/ttyUSB0")
    print("Processing First Layer")
    sendLayerType(myPort, 1)
    sendShape(myPort, 2, 2, 3, 3, 2, 2, 1, 1)
    sendInput(myPort, 1)
    sendWeight(myPort, 1)
    readOutput(myPort, 2, 2, 3, 3, 2, 2, 1, 1)

    # print("Processing Second Layer")
    # sendLayerType(myPort, 1)
    # sendShape(myPort, 2, 2, 3, 3, 2, 2, 1, 1)
    # sendInput(myPort, 1)
    # sendWeight(myPort, 2)
    # readOutput(myPort, 2, 2, 3, 3, 2, 2, 1, 1)

    closePort(myPort)


if __name__ == "__main__":
    main()
