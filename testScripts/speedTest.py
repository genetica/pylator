import threading
import cv2
import numpy as np
import time
import queue

def display(name, img, q, active_event):
    while active_event.is_set():
        cv2.imshow(name, img)
        key = cv2.waitKey(10)&0xFF
        if (key != 0) and (key != 255):
            q.put(key)
            if key == ord('q'):
                break
    cv2.destroyWindow(name)

def sine_function( value):
    return np.sin(value) / 2 + 0.5

def sine_generator(simData):
        iteration =  simData["/simulation/iteration"]
        Tt = simData["/simulation/time_step"]
        Ts = simData["/inputs/sampling_period"]
        f = simData["/inputs/frequency"]
        A = 255
        radius = 30

        height, width = simData["/inputs/height"], simData["/inputs/width"]

        signal_type = simData["/inputs/signal_type"]
        
        image = simData["image"]

        if (signal_type == "sine"):
            function = sine_function
            
        if int(iteration*Tt / Ts)*Ts >= (iteration-1)*Tt:
            time = iteration*Tt
            period = 1/f
            fraction = (time - int(time/period)*period) / period * 2*np.pi           
            output_val = A*function( fraction )

            output = cv2.circle(image,(width//2, height//2),radius, int(output_val), -1)

        else:
            output = simData["/self/previous_output"]      

        simData["/outputs/signal"] = output
        simData["/self/previous_output"] = output




if __name__ == "__main__":

    simData = {}
    iteration = 0
    simData["/simulation/iteration"] = iteration
    longestDelay = 0.0
    simData["/simulation/longestDelay"] = longestDelay
    buffer_current = 0
    simData["/simulation/buffer_current"] = buffer_current
    time_step = 0.01
    simData["/simulation/time_step"] = time_step


    sampling_period = 0.01
    simData["/inputs/sampling_period"] = sampling_period
    frequency = 1
    simData["/inputs/frequency"] = frequency
    amplitude = 1.0
    simData["/inputs/amplitude"] = amplitude
    
    noise = 0.1
    simData["/inputs/noise"] = noise

    width = 1000
    simData["/inputs/width"] = width
    height = 1000
    simData["/inputs/height"] = height

    signal_type = 'sine'
    simData["/inputs/signal_type"] = signal_type  

    simData["/2dsine_generator/outputs/signal/dim1"] = width
    simData["/2dsine_generator/outputs/signal/dim2"] = height



    simData["image"] = np.ones((1000, 1000), np.uint8)*128
    img = np.copy(simData["image"])
    simData["/outputs/signal"] = img
    avg = 0
    q = queue.Queue()
    active_event = threading.Event()
    thread = threading.Thread(target=display, args=("TestImg",img,q, active_event ))
    
    active_event.set()
    thread.start()
    for i in range(100000):
        simData["/simulation/iteration"] += 1
        t1 = time.time()
        img[:,:] = simData["/outputs/signal"]
        try:
            a = q.get(False)
        except queue.Empty:
            a = 0
            
        sine_generator(simData)
        
        t2 = time.time()
        avg += (t2 - t1)
    active_event.clear()
    print(avg/100)
