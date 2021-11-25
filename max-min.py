# HACKERRANK ANGRY CHILDREN
# PASSES ALL TESTS

def maxMin(k, arr):
    # Write your code here
    l = sorted(arr)
    minFair = min([l[i + k - 1] - l[i] for i in range(len(l)-k+1)])
    return minFair

if __name__ == '__main__':
    c =[]
    with open('problems/angrychildren/input.txt') as f:
        fl = f.readline().rstrip().split()
        n = fl[0]
        k = int(f.readline().rstrip().split()[0])
        for l in f.readlines():
            c.append(int(l))

        

    print (maxMin(k,c))
    