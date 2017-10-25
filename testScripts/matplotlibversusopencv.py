
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import cv2
import numpy as np
import time

def generate_image():
    im = np.random.random((1500, 1500))*255
    return im.astype(np.uint8)

def testCV2(N):
    wnd = cv2.namedWindow("Test")
    
    tsum = 0
    t1 = 0
    t2 = 0
    for i in range(N):
        im = generate_image()
        t1 = time.time()

        #im = cv2.resize(im, None, fx=0.6, fy=0.6)
        cv2.imshow("Test", im)
        cv2.waitKey(1)

        t2 = time.time()
        tsum += t2 - t1

    cv2.destroyAllWindows()
    tsum /= N*1.0
    print("OpenCV ", tsum)

def testPLT(N):
    plt.ion()
    fig, ax = plt.subplots()
    im = generate_image()
    im_plot = ax.imshow(im, animated=True)
    fig.canvas.draw()

    tsum = 0
    t1 = 0
    t2 = 0
    for i in range(N):
        im = generate_image()
        t1 = time.time()

        im_plot.set_data(im)
        fig.canvas.draw()      

        t2 = time.time()
        tsum += t2 - t1
    tsum /= N*1.0
    print("plt ",tsum)

def testPLT2(N):
    plt.ion()
    fig, ax = plt.subplots()
    im = generate_image()
    im_plot = ax.imshow(im, animated=True)
    fig.canvas.draw()

    background = fig.canvas.copy_from_bbox(ax.bbox)

    tsum = 0
    t1 = 0
    t2 = 0
    for i in range(N):
        im = generate_image()
        t1 = time.time()

        fig.canvas.restore_region(background)
        im_plot.set_data(im)
        ax.draw_artist(im_plot)
        fig.canvas.blit(ax.bbox)
        
        t2 = time.time()
        tsum += t2 - t1
    tsum /= N*1.0
    print("plt blit", tsum)


    

    # for x, y in user_interactions:
    #     fig.canvas.restore_region(background)
    #     points.append([x, y])
    #     scatter.set_offsets(points)
    #     ax.draw_artist(scatter)
    #     fig.canvas.blit(ax.bbox)

if __name__ == "__main__":
    testCV2(10)
    testPLT(10)
    testPLT2(10)
