# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:38:20 2022

@author: axelc
"""
import numpy as np


def Sbox(p_c_t, p_SK,p_i,alpha):
    sbox = p_c_t[0] * p_SK[p_i-1]
    sbox = sbox%16
    return int(sbox)
    
def ComputeADecipher(c_l, SK, myAlpha):
    A = np.array([[0,0,1,Sbox(c_l, SK,1, myAlpha),0],[0,Sbox(c_l, SK,2, myAlpha),0,1,0],[1,0,0,0,0],[1,0,0,0,0],[0,1,0,0,0]])
    return A

def ComputeACipher(c_t, SK, myAlpha):
    A = np.array([[0,0,1,Sbox(c_t, SK,1, myAlpha),0],[0,Sbox(c_t, SK,2, myAlpha),0,1,0],[1,0,0,0,0],[1,0,0,0,0],[0,1,0,0,0]])
    return A

def timeProductADecipher(t1,t2,c_history,SK,myAlpha):
    if t1 < t2: #Product is equal to the identity matrix of same dimension 
        M = np.identity(len(ComputeADecipher(c_history[t1],SK,myAlpha)));
    else:
        M=1
        for l in range(t1,t2):
            M = (M * ComputeADecipher(c_history[l],SK,myAlpha))%16;