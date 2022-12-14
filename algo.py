# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:47:37 2022

@author: axelc
"""
from functions import *
import numpy as np
#import pandas as pd

n = 5; #system dimension: (number of internal states)
p = 2; #Dimension of the input: Number of message to be processed in parrallel 
N_s = 2; #Total number of S-Boxes in A
SK = [6,15]; #The subkeys 
myAlpha = 0;

A_cipher = np.zeros((n,n)); #A matrix of the cipher
B_cipher = np.zeros((n,p)); #B matrix of the cipher
C_cipher = np.zeros((p,n)); #C matrix of the cipher
m_t_cipher = np.zeros((p,p)); #message vector (the input)
x_t_cipher_next = np.array([[0], [7], [3], [15], [2]]) #Cipher states which will be used as x_t for t=1


B_cipher = np.array([[0, 0], [0,0],[1,0],[0,1],[0,1]])
        
C_cipher = np.array([[1,0,0,0,0],[0, 1, 0, 0, 0]])


B_decipher = B_cipher; #The B matrix is shared
C_decipher = C_cipher; #The C matrix is shared

x_decipher_next = np.zeros((n,1)); #for the first iteration


m_init = np.array([[3, 1, 1, 13, 5, 1, 6, 7, 4],[11, 5, 2, 11, 15, 7, 12, 5, 3]]); #message vector to send
t_length = len(m_init[0]); #Number of messages to send
c_history = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]) #Allocating space for the ciphertext table

#To be verified
c_t = np.array([[0],[0]]); #For the first iteration c_t is fixed at [0;0]

#Debug
history_x_cipher = np.zeros((n,1,t_length));
history_x_decipher = np.zeros((n,1,t_length));
m_t_cipher=np.zeros((2,1))

            
            
            
            
            
for t in range(t_length): #t_length %time-loop
    print(t)
    #Cipher    
    x_t_cipher = x_t_cipher_next
    history_x_cipher[:,:,t]=x_t_cipher #for debug
    m_t_cipher = m_init[:,t] #message to cipher 
    A_cipher = ComputeACipher(c_t, SK, myAlpha) #A_cipher_K_t
    x_t_cipher_next = (A_cipher@x_t_cipher + B_cipher@m_t_cipher)%16 #Next internal state x_{t+1} eq 16
    c_t = (C_cipher@x_t_cipher)%16 #actual ciphertext c_t eq 18
    #%the cipher key is calculated from the actual iteration
    #c_history[:,t]=c_t #archive the actual ciphertext in the table
    
    #Decipher
    r= 2; #For now we consider r = 2 fixed without calculating it
    l = t-r # Variable change for simplicity
    
    if l >= 1: #in order to avoid an exeption. We wait two cycles before starting
        c_l = c_history[:,l] #input buffer of the decipher
        #A_K_ct_decipher = computeADecipher(c_l,SK,myAlpha)
        x_decipher = x_decipher_next
        history_x_decipher[:,:,l]=x_decipher # for debug
        T = (C_decipher * timeProductADecipher(t+r-1,t+1,c_history,SK,myAlpha) * B_decipher)%16 # eq 20
        T_inv = np.inv(T);
        P = (ComputeADecipher(c_t, SK, myAlpha) - B_decipher * T_inv * C_decipher * timeProductADecipher(t+r-1,t,c_history,SK,myAlpha))%16 #P(S(c_t)) eq 22
        x_decipher_next = (P * x_decipher + B_decipher * T_inv * c_l)%16 #next-state eq 21


#debug
dispHistCiph = history_x_cipher
dispHistDecip = history_x_decipher





