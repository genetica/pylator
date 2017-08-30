import math
cnt = 0
#T = int(input())
T = 1
primes = [2, 3]
for i in range(T):
    #n = (int(input()))
    n = 536870909  
    isPrime = True
    if (n == 1):
        isPrime = False   
    elif (n != 2) or (n != 3):
        maxPrimes = max(primes)
        if (maxPrimes < math.sqrt(n)):
            for i in range(maxPrimes, int(math.sqrt(n)) + 1, 2):
                isPrime = True
                for p in primes:  
                    cnt += 1                                 
                    if (i%p == 0):
                        isPrime = False
                        break
                if isPrime:
                    primes.append(i)
        print(cnt)

        isPrime = True
        for p in primes:
            cnt += 1
            if (n%p == 0):
                if (n != p):
                    isPrime = False
                break
                
        if isPrime:
            primes.append(n)
    print(cnt)                      
    if (isPrime):
        print("Prime")
    else:
        print("Not prime")