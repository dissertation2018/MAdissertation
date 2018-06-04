import numpy as np

def NMone(A):
    l = len(A[:,0])
    #create permutation of graph, that is, isomorphic to original
    I = np.identity(l)
    r = np.arange(l)
    np.random.shuffle(r)
    perm = np.zeros([l,l])
    for i in range(0,l):
        perm[i,:] = I[:,r[i]]

    Ap = np.dot(perm.transpose(),np.dot(A,perm))
        
    #find degree distribution of recipricol, in and out
    
    Ap_rec = np.multiply(Ap,Ap.transpose())
    Ap_dir = Ap - Ap_rec
    deg_out = np.zeros(l)
    deg_in = np.zeros(l)
    for i in range(0,l):
        deg_in[i] = sum(Ap_dir[i,:])
        deg_out[i] = sum(Ap_dir[:,i])
    
    #symmetrize
    Ap_sy = Ap
    #rewire symmetrized network, maintaining degree distribution
    E1 = np.where(Ap_rec == 1)[0]
    E2 = np.where(Ap_rec == 1)[1]
    it = 500 #iterations
    for k in range(0,it):
        E1 = np.where(Ap_rec == 1)[0]
        E2 = np.where(Ap_rec == 1)[1]
        ch = np.arange(len(E1))
        e1 = np.random.choice(ch)
        ch = np.delete(ch, np.where(ch==e1)[0])
        e2 = np.random.choice(ch)
        if E1[e1]==E2[e2] or E2[e1]==E1[e2]:
            continue   
        elif Ap_sy[E1[e1],E2[e1]]==0 or Ap_sy[E1[e2],E2[e2]]==0 or Ap_sy[E1[e1],E2[e2]]==1 or Ap_sy[E1[e2],E2[e1]]==1 or Ap_sy[E2[e2],E1[e1]]==1 or Ap_sy[E2[e1],E1[e2]]==1:
            continue  
        else:
            Ap_sy[E1[e1],E2[e1]]=0
            Ap_sy[E2[e1],E1[e1]]=0
            Ap_sy[E1[e2],E2[e2]]=0
            Ap_sy[E2[e2],E1[e2]]=0
    
            Ap_sy[E1[e1],E2[e2]]=1
            Ap_sy[E2[e2],E1[e1]]=1
            Ap_sy[E1[e2],E2[e1]]=1
            Ap_sy[E2[e1],E1[e2]]=1
        
        Ap_rec= np.multiply(Ap_sy, Ap_sy.transpose())
        #print Ap_sy    
        #choose reciprocal edge to delete one direction based on in and out degree of each node
    j = np.count_nonzero(deg_out)
    #print deg_out
    Ap_dir = Ap_sy-Ap_rec
    for k in range(0,it):
        E1 = np.where(Ap_dir == 1)[0]
        E2 = np.where(Ap_dir == 1)[1]
        ch = np.arange(len(E1))
        e1 = np.random.choice(ch)
        ch = np.delete(ch, np.where(ch==e1)[0])
        e2 = np.random.choice(ch)
        if E1[e1]==E2[e2] or E2[e1]==E1[e2]:
            continue   
        elif Ap_sy[E1[e1],E2[e1]]==0 or Ap_sy[E1[e2],E2[e2]]==0 or Ap_sy[E1[e1],E2[e2]]==1 or Ap_sy[E1[e2],E2[e1]]==1 or Ap_sy[E2[e1],E1[e2]]==1 or Ap_sy[E2[e2],E1[e1]]==1:
            continue  
        else:
            #print 3
            Ap_sy[E1[e1],E2[e1]]=0
            Ap_sy[E1[e2],E2[e2]]=0

            Ap_sy[E1[e1],E2[e2]]=1
            Ap_sy[E1[e2],E2[e1]]=1
            
        Ap_dir = Ap_sy - Ap_rec
        
    return Ap_sy