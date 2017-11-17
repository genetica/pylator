import cv2
import numpy as np

im = np.random.randint(0,2**14, width*height, np.uint16)



def 
        hist = cv2.calcHist([hist_img],[0],None,[256],[0,256])
        hist[0] = 0
        if (simData["/" + self.name + '/histoLog'] == True):
            hist = np.log10(hist + 1)
        if (hist.max() != 0):
            hist = np.array(hist/hist.max() * (hist_h - 1), np.int)
        else:
            hist = np.array(hist * (hist_h - 1), np.int)
        for i in range(256):
            if (hist[i] > 0):
                col[0:int(hist[i])] = 1.0
                col[int(hist[i]):] = background
            else:
                col[:] = background
            fig[:,int(2*i),:] = np.array([col.transpose()*255.0,col.transpose()*255.0,col.transpose()*255.0], np.uint8).transpose()
            fig[:,int(2*i+1),:] = np.array([col.transpose(),col.transpose()*255.0,col.transpose()],np.uint8).transpose()
        
        output[:hist_h,:hist_w,:] = fig[::-1,:,:]


def
    #Create an empty image for the histogram
    h = np.zeros((hist_height,hist_width))

    #Create array for the bins
    bins = np.arange(nbins,dtype=np.int32).reshape(nbins,1)

    while True:
    # grab the current frame 
    (grabbed, frame) = camera.read()

    if not grabbed:
        "Camera could not be started."
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #Calculate and normalise the histogram
    hist_hue = cv2.calcHist([hsv],[0],mask,[nbins],[0,256])
    cv2.normalize(hist_hue,hist_hue,hist_height,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_hue))
    pts = np.column_stack((bins,hist))

    #Loop through each bin and plot the rectangle in white
    for x,y in enumerate(hist):
        cv2.rectangle(h,(x*bin_width,y),(x*bin_width + bin_width-1,hist_height),(255),-1)

    #Flip upside down
    h=np.flipud(h)


def

    line1.set_ydata(np.cos(2 * np.pi * (x1+i*3.14/2) ) * np.exp(-x1) )

    # redraw the canvas
    fig.canvas.draw()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)   