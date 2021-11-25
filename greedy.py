# HACKERRANK GREEDY FLORIST
# PASSES ALL TESTS

def getMinimumCost(k, c):
    flb = len(c)
    l = sorted(c)[::-1] # sort and reverse
    cost = 0
    i = 1
    while flb > k:
        cost += sum(l[:k]*i) 
        l = l[k:]
        i +=1
        flb = len(l)

    cost += sum(l[:k]*i) # pick up letf - over items
    
    return  cost

if __name__ == '__main__':
    c =[]
    with open('problems/greedy_florist/input.txt') as f:
        fl = f.readline().rstrip().split()
        n = fl[0]
        k = int(fl[1])

        l = f.readline().rstrip().split()
        c = [int(i) for i in l]
        

    print (getMinimumCost(k,c))
    