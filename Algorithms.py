'''
Created on May 5, 2017

@author: _jhoman
'''

def merge_sort(A):
    
    if len(A) == 1:
        
        return A
    
    n = int(len(A)/2)
    
    a = merge_sort(A[:n])
    b = merge_sort(A[n:])
    
    c = []
    
    while(len(a) > 0 and len(b) > 0):
        
        if a[0] <= b[0]:
            
            c.append(a[0])
            a = a[1:]
        
        else:
            c.append(b[0])
            b = b[1:]
           
    for val in a:
        
        c.append(val)
        
    for val in b:
        
        c.append(val)
        
    return c

def quick_sort(A):
    
    if len(A) <= 1:
        
        return A
    
    L = []
    G = []
    E = []
    
    pivot = A[-1]
    
    for i in range(len(A)):
        
        if A[i] < pivot:
            
            L.append(A[i])
            
        elif A[i] > pivot:
            
            G.append(A[i])
            
        else:
            
            E.append(A[i])
        
    L = quick_sort(L)
    G = quick_sort(G)
    
    S = []
    
    for k in range(len(L)):
        
        S.append(L[k])
        
    for k in range(len(E)):
        
        S.append(E[k])
        
    for k in range(len(G)):
        
        S.append(G[k])
        
    return S


def quick_select(S,k):
    import numpy as np
    
    if len(S) == 1:
        
        return S[0]
    
    L = []
    E = []
    G = []
    
    i = np.random.randint(0,len(S)) 
    
    pivot = S[i]
    
    for i in range(len(S)):
        
        if S[i] < pivot:
            
            L.append(S[i])
            
        elif S[i] > pivot:
            
            G.append(S[i])
            
        else:
            
            E.append(S[i])
        
    if k <= len(L):
        
        return quick_select(L,k)
    
    elif k <= len(E) + len(L):
        
        return pivot
    
    else:
        
        return quick_select(G,k-(len(L) + len(E)))


if __name__ == '__main__':
    print("Merge Sort:",*merge_sort([1,5,4,2,6,4,9,8,7]))
    print("Quick Sort:",*quick_sort([1,5,8,4,2,8,6,9,7]))
    print("Quick Select:",quick_select([1,5,8,4,2,3,8,6,9,7],3))
    