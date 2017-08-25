import socket
import cv2
import numpy as np
import time
 
def getCameraIP():
    host = ' '
    port = 1987

    ipSocket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ipSocket.bind((host, port))

    m = ipSocket.recvfrom(1024)

    ipSocket.close()

    return m[1][0]

def createIn(byte1, byte2):
    return (int(byte1) << 8) | int(byte2)


def Main():
    height, width = 512, 640

    cv2.namedWindow("Output")
    imgFlat = np.zeros(height*width)


## Create Server
    hostReady = "192.168.2.100"
    portReady = 4957
     
    # Set server connection
    readySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Assign port and id to Server
    readySocket.bind((hostReady,portReady))
    # Set amount of connections to server
    readySocket.listen()
    conn, addr = readySocket.accept()
    print ("Connection from: " + str(addr))

## Connect to camera
    host = getCameraIP()
    port = 4956
         
    dataSocket =  socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dataSocket.connect((host,port))

## Start receiving
    print("Start Imaging")
    t2 = 0
    while True:
        # Measure Frames per Second
        t1 = time.clock()
        diff = t1 - t2
        t2 = t1
        print("\rFPS: ", 1.0/diff, end="")   

        # Server send ready
        conn.send("R".encode())

        NOP = 0
        frameRX = False

        while frameRX:
            data = dataSocket.recv(4096)
            
            if (len(data) > 10):
                block = (data[1] << 24) | (data[2] << 16) |(data[3] << 8) |(data[4])

                N = (len(data) - 4 - 2)/2 #Start byte, end byte, 4 bytes for block number

                data = data[-N-1:-1]

                imgFlat[block*N : (block+1)*N] = np.array(list(map(createInt, data[::2], data[1::2])))
            else:
                if NOP == 0:
                    NOP = (data[1] << 24) | (data[2] << 16) |(data[3] << 8) |(data[4])
                else:
                    frameRX = True

        img = np.resize(imgFlat, (height, width))
        cv2.imshow("Output", img)
        key = cv2.waitKey(20) & 0xFF
        
        if (key == 27):
            break
            
    conn.close()
    dataSocket.close()
    cv2.destroyAllWindows()
     
if __name__ == '__main__':
    Main()

