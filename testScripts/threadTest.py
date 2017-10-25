import threading
import cv2
import numpy as np
import time
import queue

def display(name, img, q):
    while active_event.is_set():
        cv2.imshow(name, img)
        key = cv2.waitKey(1)&0xFF
        if (key != 0) and (key != 255):
            q.put(key)       
    cv2.destroyWindow(name)

if __name__ == "__main__":
    img = np.zeros((1000, 1000), np.uint8)
    avg = 0
    q = queue.Queue()
    thread = threading.Thread(target=display, args=(img,q, ))
    active_event = threading.Event()
    active_event.set()
    thread.start()
    for i in range(100):
        img[:,:] = 0
        img[5*i:10*i, :] = 255
        t1 = time.time()
        
        time.sleep(0.02)
        try:
            a = q.get(False)
            print(a)
        except queue.Empty:
            a = 0
            
            
        
        t2 = time.time()
        avg += (t2 - t1)
    active_event.clear()
    print(avg/100)
