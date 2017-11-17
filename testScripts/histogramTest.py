###############################################################################
#
# Test to see whether numpy or opencv produce the quickest histogram
# cv2.calcHist
# np.bincount
#
# Conclusion:
#    Opencv is significantly faster than numpy
#    > OpenCV 1.0
#    > Numpy  1.43384
#
###############################################################################

import cv2
import numpy as np
import time
width, height = 1000, 1000
N = 10
iterations = 100

avg_lst =[0.0001,0.0001]

for k in range(iterations):
    
    avg = 0
    for i in range(N):
        im = np.random.randint(0,2**14, width*height, np.uint16)
        t1 = time.time()
        hist_np = np.bincount(im.reshape(-1))
        t2 = time.time()
        avg += t2 - t1
    avg_lst[1] += avg/N
    
    avg = 0
    for i in range(N):
        im = np.random.randint(0,2**14, width*height, np.uint16)
        t1 = time.time()
        hist_cv2 = cv2.calcHist([im],[0],None,[2**14],[0,2**14])
        t2 = time.time()
        avg += t2 - t1
    avg_lst[0] += avg/N


print("OpenCV {}".format(avg_lst[0]/min(avg_lst)))
print("Numpy  {}".format(avg_lst[1]/min(avg_lst)))