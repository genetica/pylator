import pylator as pyl
import multiprocessing as mp
import numpy as np
import time
import threading
import queue
import cv2

crit = mp.get_logger().critical
info = mp.get_logger().info
debug = mp.get_logger().debug

def module_configuration():
    simData = {
    # Define Module Outputs

    # Define module inputs with assigned defaults
    "/inputs/monitor" : [],
    "/inputs/signal1"  : 0
    }
    return simData

class Module(pyl.Model):
    def mouse_callback(self, event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix,self.iy = x,y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.cx, self.cy = x, y
                #if mode == True:
                #for monitor in self.moduleData["/self/monitor"]:
                #    self.image[monitor][:,:,:] = cv2.cvtColor(self.image_rx[monitor], cv2.COLOR_GRAY2RGB)
                #    cv2.rectangle(self.image[monitor],(self.ix,self.iy),(x,y),(0,255,0),-1)
                #else:
                    #cv2.circle(img,(x,y),5,(0,0,255),-1)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            #for monitor in self.moduleData["/self/monitor"]:
            #    self.image[monitor][:,:,:] = cv2.cvtColor(self.image_rx[monitor], cv2.COLOR_GRAY2RGB)
            #    cv2.rectangle(self.image[monitor],(self.ix,self.iy),(x,y),(0,255,0),-1)

    def display(self, name_lst, img_lst, q, active_event):
        self.ix = 0
        self.iy = 0
        self.cx = 0
        self.cy = 0
        self.drawing = False

        for monitor in name_lst:
            cv2.namedWindow(monitor)
            cv2.setMouseCallback(monitor,self.mouse_callback)
        
        while active_event.is_set():
            for monitor in name_lst:
                self.image[monitor][:,:,:] = cv2.cvtColor(self.image_rx[monitor], cv2.COLOR_GRAY2RGB)
                if self.drawing == True:
                    cv2.rectangle(self.image[monitor],(self.ix,self.iy),(self.cx,self.cy),(0,255,0),-1)

            for monitor in name_lst:
                cv2.imshow(monitor, self.image[monitor])
            key = cv2.waitKey(10)&0xFF
            if (key != 0) and (key != 255):
                q.put(key)
                if key == ord('q'):
                    break
        for monitor in name_lst:                
            cv2.destroyWindow(monitor)

     
    def initialise(self, simData):

        self.q = queue.Queue()
        self.active_event = threading.Event()
        
        self.image = {}
        self.image_rx = {}
        self.thread = {}

        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            self.image_rx[monitor] = np.copy(simData["/inputs/signal" +str(idx + 1)])

        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            self.image[monitor] = cv2.cvtColor(simData["/inputs/signal" + str(idx + 1)], cv2.COLOR_GRAY2RGB)


        #cv2.setMouseCallback('image',draw_circle)

        self.thread = threading.Thread(target=self.display, args=(simData["/inputs/monitor"], self.image, self.q, self.active_event, ))
       
        self.active_event.set()
        self.thread.start()

        time_step = simData["/simulation/time_step"]

    def execute(self, simData):
        
        debug("Executing my Model {} Iteration {}".format(self.name, simData["/simulation/iteration"]))

        for idx, monitor in enumerate(simData["/inputs/monitor"]):
            self.image_rx[monitor][:,:] = np.copy(simData["/inputs/signal" + str(idx + 1)])

        try:
            key = self.q.get(False)
        except queue.Empty:
            key = 0

        simData["/inputs/keypress"] = key
        if key==ord('q'):
            self.flags["simulation_stop"].set()

    def finalise(self, simData):
        self.active_event.clear()
        info("Waiting")
        self.thread.join(0.5)
        info("Done")

if __name__ == "__main__":
    pass