import numpy as np

#A= np.array([[0,1,0,1],[0,0,1,0],[1,1,0,1],[0,1,1,0]])
#A2 = np.array([[0,1,1,0],[0,0,1,0],[1,1,0,1],[0,0,1,0]])
#A is structural network
#A2 is functional network

def NM2(A, A2):
    A_same = np.multiply(A,A2)
    A_FP = A2 - A_same
    A_FN = A - A_same
    #obtain number of false positives and false negatives
    FP = np.count_nonzero(A_FP)
    FN = np.count_nonzero(A_FN)

    A_rand = np.dot(A, np.identity(len(A[:,0])))
    E_1 = np.where(A==0)[0] #E_1 and E_2 are locations of all zeros in structural adjacency matrix
    E_2 = np.where(A==0)[1]
    c = np.arange(len(E_1))#list of edges
    #randomly add false positives in the structural network
    while FP > 0:
        ch = np.random.choice(c)#randomly chooses an edge
        if E_1[ch] == E_2[ch]:
            continue
        else:
            A_rand[E_1[ch],E_2[ch]]=1
            c = np.delete(c,np.where(c==ch)[0])
            FP = FP-1
            
    #randomly assign false negatives   
    EN_1 = np.where(A==1)[0] #E_1 and E_2 are locations of all edges in structural network
    EN_2 = np.where(A==1)[1]
    c = np.arange(len(EN_1))
    while FN>0:
        ch = np.random.choice(c)
        #print ch
        if EN_1[ch] == EN_2[ch]:
            continue
        else:
            A_rand[EN_1[ch],EN_2[ch]]=0
            c = np.delete(c,np.where(c==ch)[0])
	    FN=FN-1

    return A_rand