import multiprocessing as mp
import numpy as np
import ctypes

my = "asd"

a = mp.RawArray(ctypes.c_wchar, 3)
a[:3] = my
print(a)
print(a[:])
b = np.frombuffer(a, np.uint16)
f = np.vectorize(chr)
print(b)
print("".join(f(b)))
a[:] = "we"
print(a)
print(a[:])
b = np.frombuffer(a, np.uint16)
print("".join(f(b)))

print("VALUE")

# my = "asd"

# a = mp.RawValue(ctypes.c_wchar_p, my)

# print(a)
# print(a.value)
# b = np.frombuffer(a, np.uint8)
# print(b)
# a.value = "we"
# print(a)
# print(a.value)
# b = np.frombuffer(a, np.uint8)
# print(b)
