import math

cnt = 0

def isPrime(n):
    global cnt
    if n == 2:
        return True
    elif n == 1 or (n & 1) == 0:
        return False
        
    for i in range(3, math.ceil(math.sqrt(n)) + 1, 2):
        cnt += 1
        if (n % i) == 0:
            return False
    
    return True

#p = int(input())
p = 1
for i in range(0, p):
    #x = int(input())
    x = 536870909

    s = "Prime" if (isPrime(x)) else "Not prime"
    print(cnt)
    print(s)
    