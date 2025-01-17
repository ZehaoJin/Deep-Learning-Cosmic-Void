# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 00:08:07 2019

@author: zehaojin
"""
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt




def Cloud_in_Cell(gal_list,N=1050):
    #N = 1050
    X_g=np.linspace(0,N-1,N)#0,1,2,3,...,1049
    grid_size = len(X_g)#1050
    Y_g=np.linspace(0,N-1,N)#same as X
    Z_g=np.linspace(0,N-1,N)#same as X

    rho_field = np.zeros((N,N,N))


    mu, sigma = N/2, 15 # mean and standard deviation


    #f =  sigma *npr.randn(n,3) + mu
    #f = SO_list[:, :3]#first 3 columns
    f = gal_list
    #print(f)
    w_x = f[:, 0] - np.floor(f[:, 0])#205.07-205=0.07
    w_y = f[:, 1] - np.floor(f[:, 1])
    w_z = f[:, 2] - np.floor(f[:, 2])

    #get conjugate weight
    t_x = 1. - w_x
    t_y = 1. - w_y
    t_z = 1. - w_z

    #get particle indices
    ptcl_idx = f.astype(int)#same as floor?
    #print(ptcl_idx)
    #print(type(ptcl_idx))

    ptcl_idx = ptcl_idx % 1050#maybe % N?


    #for idx in range(10):#range(len(ptcl_idx)):
    for idx in range(len(ptcl_idx)):
        i, j, k = ptcl_idx[idx, :]
        #print(i, j, k)
        i1, j1, k1 = (ptcl_idx[idx, :] + 1) % N#i+1,j+1,k+1
        #print(i1, j1, k1)
        rho_field[i, j, k] += t_x[idx] *t_y[idx] *t_z[idx]###i->t i1->w, with all combinations
        rho_field[i, j, k1] += t_x[idx] *t_y[idx] *w_z[idx]
        rho_field[i, j1, k] += t_x[idx] *w_y[idx] *t_z[idx]
        rho_field[i, j1, k1] += t_x[idx] *w_y[idx] *w_z[idx]

        rho_field[i1, j, k] += w_x[idx] *t_y[idx] *t_z[idx]
        rho_field[i1, j, k1] += w_x[idx] *t_y[idx] *w_z[idx]
        rho_field[i1, j1, k] += w_x[idx] *w_y[idx] *t_z[idx]
        rho_field[i1, j1, k1] += w_x[idx] *w_y[idx] *w_z[idx]
    return rho_field

def target2density(x_t,y_t,N_GRID,n_grid):
    N, n = N_GRID,n_grid
    x, y = np.meshgrid(np.linspace(-1,1,n), np.linspace(-1,1,n))
    d = np.sqrt(x*x+y*y)
    sigma, mu = 0.1, 0.0
    g = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )
    #y_t, x_t = int(y_t), int(x_t)\
    y_t, x_t = int(y_t), int(x_t)
    G = np.zeros((N,N))
#     print("old pos", x_t, y_t)
#     #y_t, x_t = (y_t/0.02)/112, (x_t/0.02)/224
#     print("mid pos", x_t, y_t)
# #     y_t *= 0.02
# #     x_t *= 0.02
#     y_t = int(N/2 + y_t*N/2)
#     x_t = int(N/2 + x_t*N/2)
#     print("new pos", x_t, y_t)
#     print("old pos", x_t, y_t)
#     y_t = int(y_t/0.02) + 112
#     x_t = int(x_t/0.02) + 112
#     y_t = int(y_t/4)
#     x_t = int(x_t/4)
#     print("new pos", x_t, y_t)
    grid_shape = G[y_t-n//2:y_t+1+n//2,x_t-n//2:x_t+1+n//2].shape

    G[y_t-n//2:y_t+1+n//2,x_t-n//2:x_t+1+n//2] = g[:grid_shape[0],:grid_shape[1]]

    return G

print('generating rho_field...')
rho_field=Cloud_in_Cell(gal_list=np.loadtxt('void_project/data/gal_list'),N=1050)

max_step=1050
step_interval=37
#data_set_dimension=22
data_set_dimension=22
#22*37=814
#1050-224=826
#22^3=10648


#for ind in range(total_num_of_datasets):
#gal_map_set=np.zeros((steps_each_run*max_step*max_step,224,224))
gal_map_set=np.zeros((data_set_dimension**3,224,224))
for i in range(data_set_dimension):
    #print('gal_map',i,'of 22')
    for j in range(data_set_dimension):
        for k in range(data_set_dimension):
            gal_map_set[i*data_set_dimension*data_set_dimension+j*data_set_dimension+k] = np.sum(rho_field[i*step_interval:i*step_interval+224,j*step_interval:j*step_interval+224,k*step_interval:k*step_interval+224], axis=2)
    #np.save('./gal_map_set_{}.npy'.format(ind),gal_map_set)
    #gal_map_set=None
rho_field=None

SO_list=np.loadtxt('void_project/data/SO_list')
#for ind in range(total_num_of_datasets):
void_map_set=np.zeros((data_set_dimension**3,224,224))
for i in range(data_set_dimension):
    #print('void_map',i,'of 22')
    for j in range(data_set_dimension):
        for k in range(data_set_dimension):
            sub=SO_list[((i*step_interval)<=SO_list[:,0])&(SO_list[:,0]<(i*step_interval+224))&((j*step_interval)<=SO_list[:,1])&(SO_list[:,1]<(j*step_interval+224))&((k*step_interval)<=SO_list[:,2])&(SO_list[:,2]<(k*step_interval+224))&(SO_list[:,3]>10)]
            for z in range(sub[:,0].size):
                void_map_set[i*data_set_dimension*data_set_dimension+j*data_set_dimension+k] += target2density((sub[z,0]-(i*step_interval)),(sub[z,1]-(j*step_interval)),224,7)
            #print(np.sum(void_map_set[i*data_set_dimension*data_set_dimension+j*data_set_dimension+k]))
    #np.save('./void_map_set_{}.npy'.format(ind),void_map_set)
    #void_map_set=None
SO_list=None

#seperate train and test
from sklearn.model_selection import train_test_split
test_size=0.2

print('seperating train and test...')
xTrain, xTest, yTrain, yTest = train_test_split(gal_map_set,void_map_set,test_size = test_size)

#check
print(xTrain.shape, xTest.shape, yTrain.shape, yTest.shape)


np.save('void_project/data/xTrain.npy',xTrain)
np.save('void_project/data/yTrain.npy',yTrain)
np.save('void_project/data/xTest.npy',xTest)
np.save('void_project/data/yTest.npy',yTest)


a=yTest
print(a.shape)
print(np.sum(a[0]))
print(np.sum(a[1]))
print(np.sum(a[2]))
print(np.sum(a[3]))
