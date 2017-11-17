###############################################################################
# Tests to see if string concatenation is slower or faster than 
# the .format function.
#
# Conclusion.
#   Using variables does slow string creation down(+-5%) but the difference
#   between concatenation and .format function is not statistically 
#   significant. .format is slower than the str() function for floats
#   as it apply more formatting to the number than the str() function.
#
###############################################################################

import time


text1 = "Toets hier"
text2 = "Nog so bietjie"
N = 100000
iterations = 100
avg = 0
avg_lst = [0,0,0,0]

for k in range(iterations):

    avg = 0
    t1 = time.time()
    for i in range(N):
        text = "Toets hier" + str(i*0.1) +  "Nog so bietjie" 
    t2 = time.time()
    avg += t2 - t1
    avg_lst[2] += avg
    #print("{}".format(avg/N))

    avg = 0
    t1 = time.time()
    for i in range(N):
        text = text1 + str(i*0.1) + text2 
    t2 = time.time()
    avg += t2 - t1
    avg_lst[0] += avg

    avg = 0
    t1 = time.time()
    for i in range(N):
        text = "{} {} {}".format("Toets hier",i*0.1, "Nog so bietjie")
    t2 = time.time()
    avg += t2 - t1
    avg_lst[3] += avg     

    #print("{}".format(avg/N))

    avg = 0
    t1 = time.time()
    for i in range(N):
        text = "{} {} {}".format(text1,i*0.1,text2)
    t2 = time.time()
    avg += t2 - t1
    avg_lst[1] += avg
    #print("{}".format(avg/N))





    #print("{}".format(avg/N))

for i in range(4):
    avg_lst[i] = avg_lst[i]/iterations


print("Variable String Addition: {}".format(avg_lst[0]/min(avg_lst)))
print("Variable Format function: {}".format(avg_lst[1]/min(avg_lst)))
print("         String Addition: {}".format(avg_lst[2]/min(avg_lst)))
print("         Format function: {}".format(avg_lst[3]/min(avg_lst)))
