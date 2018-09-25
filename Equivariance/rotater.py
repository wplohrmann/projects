#!/usr/local/Cluster-Apps/python/3.5.1/bin/python3
import numpy as np
import h5py

Cs = np.array([[0.1134252802,   -0.1672312403,    0.0132130968],
      [-0.1679228708,   -2.0335650262,   -0.7755985884],
      [-0.2471752907,   -3.1005679779,    0.352375911],
      [0.8339661008,   -3.0326692352,    1.4649830643],
      [-0.075411507,    -2.0656424325,    2.2914206619],
      [-1.1598446223,   -2.1332571476,    1.181105299],
      [-1.0922960103,   -1.0774638867,    0.016893457]])
                                    
Hs = np.array([[1.3241802523,    1.2613006699,   0.216794625],
      [-0.3062292208,   -2.3351845093,  -1.8138084687],
      [-0.5787837425, -4.0856536715,  0.0216777754],
      [1.0032693684,    -3.9952209982,  1.9519167544],
      [1.7952897582,  -2.6260644727,  1.1470955522],
      [-0.4102306046,   -2.4895263941,  3.2408853495],
      [0.3324635063,  -1.0715100853,  2.4855020729],
      [-2.1736012478,   -2.3969713055,  1.4813219599],
      [-2.0320623722, -0.6692214683,  -0.3490222455]])
                                                                  
Os = np.array([[0.9317161256,   -1.0744217617,   -0.6503009117]])
                                                                                
Ns = np.array([[0.3601600971,    0.9919911933,    0.422505935]])

positions = np.vstack((Cs,Hs,Os,Ns))

biggest = np.max(positions, axis=0)
smallest = np.min(positions, axis=0)
mean = (biggest+smallest)/2
Cs -= mean
Hs -= mean
Os -= mean
Ns -= mean
    
def rotatez(arr,theta):
    cos = np.cos(theta)
    sin = np.sin(theta)
    x = np.copy(arr[:,0:1])
    y = np.copy(arr[:,1:2])
    z = np.copy(arr[:,2:])
    x_ = cos*x-sin*y
    y_ = cos*y+sin*x
    z_ = z
    arr_ = np.concatenate((x_,y_,z_),axis=1)
    assert arr_.shape==arr.shape
    return arr_

def rotatey(arr,theta):
    cos = np.cos(theta)
    sin = np.sin(theta)
    x = np.copy(arr[:,0:1])
    y = np.copy(arr[:,1:2])
    z = np.copy(arr[:,2:])
    x_ = cos*x-sin*z
    y_ = y
    z_ = cos*z+sin*x
    arr_ = np.concatenate((x_,y_,z_),axis=1)
    assert arr_.shape==arr.shape
    return arr_

def rotate(arr,theta1,theta2,theta3):
    return rotatez(rotatey(rotatez(arr,theta1), theta2), theta3)
    
    

#Specifying the input
#20x20x20 grid
grid_size = 6.5 # Side length in Å of box
grid_resolution = 32 # 20x20x20 boxes
atoms = 4 # CHON

x = np.linspace(-grid_size,grid_size, grid_resolution)
xx,yy,zz = np.meshgrid(x, x, x)

radii = np.array([0.75, 0.31, 0.66, 0.71, 0.57])
atom_types = {'C': 0, 'H': 1, 'O': 2, 'N': 3, 'F': 4} 

for k in range(100):
    
    image = np.zeros((grid_resolution,grid_resolution,grid_resolution, atoms))
    
    theta1, theta2, theta3 = 2*np.pi * np.random.rand(3)
    Cs = rotate(Cs,theta1,theta2,theta3)
    Hs = rotate(Hs,theta1,theta2,theta3)
    Os = rotate(Os,theta1,theta2,theta3)
    Ns = rotate(Ns,theta1,theta2,theta3)
    


    for n in range(Cs.shape[0]):
        x_pos,y_pos,z_pos = Cs[n]
        radius = radii[0]
        addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
        image[:, :, :, 0] += addition/np.sum(addition)

    for n in range(Hs.shape[0]):
        x_pos,y_pos,z_pos = Hs[n]
        radius = radii[1]
        addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
        image[:, :, :, 1] += addition/np.sum(addition)

    for n in range(Os.shape[0]):
        x_pos,y_pos,z_pos = Os[n]
        radius = radii[2]
        addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
        image[:, :, :, 2] += addition/np.sum(addition)

    for n in range(Ns.shape[0]):
        x_pos,y_pos,z_pos = Ns[n]
        radius = radii[3]
        addition = np.exp(-0.5*((xx-x_pos)**2+(yy-y_pos)**2+(zz-z_pos)**2)/radius**2)
        image[:, :, :, 3] += addition/np.sum(addition)
    
    with h5py.File('rotated.hdf5', 'r+') as f:
        images = f['image']
        images[k] = image
