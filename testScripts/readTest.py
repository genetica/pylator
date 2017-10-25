import time

N = 10000
avg = 0

for i in range(N):
    a = []
    a.append(0)
    t1 = time.time()
    for i in range(1, 1000):
        a.append(a[i-1] + i)
    t2 = time.time()
    avg += (t2 - t1)
print(avg/N)

avg = 0
for i in range(N):
    a = {}
    a[0] = 0
    t1 = time.time()
    for i in range(1, 1000):
        a[i] = a[i-1] + i
    t2 = time.time()
    avg += (t2 - t1)
print(avg/N)