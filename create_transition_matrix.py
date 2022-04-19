import numpy as np
from numpy import ndarray as nda

def ctm(p,d,k):

    if d==0 and k==0:
        transition_matrix = np.array([[p, 1-p],[1-p, p]])
    
    else: 
        p_trans = nda.flatten(p*np.ones((1,k-d))) 
        p0 = np.concatenate([np.ones(d), p_trans])
        p1 = np.ones((1,k)) - p0   
    
        P11_a = np.array(np.zeros((1,np.size(p1,1)))).T
        P11_b = np.diag(p0)
        P11_ab = np.append(P11_a,P11_b, axis = 1)
        P11_c = np.concatenate([np.zeros(1),nda.flatten(np.zeros((1,k)))])
        P11 = np.append(P11_ab.T, np.array([P11_c]).T,axis=1).T
        P01 = np.zeros((k+1,k+1))
        P01[k,0] = 1 
        P01[0:k,0] = p1
        
        transition_matrix = np.vstack((np.hstack((P11,P01)), np.hstack((P01,P11))))
    
    return transition_matrix