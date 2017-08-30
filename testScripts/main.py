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

def createInt(byte1, byte2):
    return (int(byte1) << 8) | int(byte2)


def Main():
    height, width = 512, 640

    cv2.namedWindow("Output")
    imgFlat = np.zeros(height*width)


## Create Server
    hostReady = "192.168.2.100"
    hostReady = " "
    portReady = 4957
     
    # Set server connection
    readySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Assign port and id to Server
    #readySocket.bind((hostReady,portReady))
    # Set amount of connections to server
    #readySocket.listen()
    #conn, addr = readySocket.accept()
    #print ("Connection from: " + str(addr))
    print(readySocket)
## Connect to camera
    hostData = getCameraIP()
    #hostData = " "
    portData = 4956
    


    dataSocket =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #dataSocket.settimeout(1)
    dataSocket.connect((hostData,portData))
    #dataSocket.bind((hostData,portData))
    
    print(dataSocket)
## Start receiving
    print("Start Imaging")
    t2 = 0
    while True:
        # Measure Frames per Second
        t1 = time.clock()
        diff = t1 - t2
        t2 = t1
        
        #print("\rFPS: ", 1.0/diff, end="")   

        # Server send ready
#        readySocket.sendto("R".encode(), (hostReady,portReady))

        NOP = 0
        frameRX = True
        imgFlat = np.zeros(height*width)
        block = 0
        while frameRX:
#            try:
            data = []
            tyd = []
            cont = True
            cnt = 0
            while cont:
                t1 = time.clock()
                diff = t1 - t2
                t2 = t1                
                rx = dataSocket.recv(4096)
                #data.append(rx)
                #tyd.append(diff)
                print(diff)
                cnt += 1
                if (diff > 1):
                   
                   print(cnt) 
                   cnt = 0

                
            #data = dataSocket.recv(4096)
            print(len(data))
            for i in tyd:
                print(i)
            #print(data)
            NOP += 1
  #          except:
   #             break
            frameRX = False
            
            if (NOP > 512):
                #block = (data[1] << 24) | (data[2] << 16) |(data[3] << 8) |(data[4])
                block += 1
                #N = (len(data) - 4 - 2)/2 #Start byte, end byte, 4 bytes for block number
                N = len(data)/2
                #data = data[int(-N-1):-1]
                imgFlat = np.array(list(map(createInt, data[::2], data[1::2])))
                img = np.resize(imgFlat, (height, width))
                img = np.array((img/img.max()*255), np.uint8)

                print(NOP, new.shape)
                imgFlat[int(block*N) : int((block+1)*N) ] = new
                #imgFlat[int(block*N) : int((block+1)*N/2) ] = np.array(list(map(createInt, data[::2], data[1::2])))
            else:
                if NOP > 2:
                    frameRX = False
                #if NOP == 0:
                #    NOP = (data[1] << 24) | (data[2] << 16) |(data[3] << 8) |(data[4])
                #else:
                #    frameRX = False

        img = np.resize(imgFlat, (height, width))
        img = np.array((img/img.max()*255), np.uint8)
        cv2.imshow("Output", img)
        print(img)
        key = cv2.waitKey(1) & 0xFF
        
        if (key == 27):
            break
            
    readySocket.close()
    dataSocket.close()
    cv2.destroyAllWindows()
     
if __name__ == '__main__':
    Main()

