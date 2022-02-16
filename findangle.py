import numpy as np

roll = np.pi/2
pitch = 0
yaw = 0

phi = pitch+yaw
theta = roll+yaw
psi = roll+pitch

Rx = np.array([[1,0,0],[0,np.cos(phi),-np.sin(phi)],[0,np.sin(phi),np.cos(phi)]])
Ry = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]])
Rz = np.array([[np.cos(psi),-np.sin(psi),0],[np.sin(psi),np.cos(psi),0],[0,0,1]])

rotmat=np.matmul(np.matmul(Rx,Ry),Rz)

rotmateig = np.linalg.eig(rotmat)

j=0

for i in rotmateig[0]:
    if np.isreal(i):
        j=i
        break

rmeigvec = rotmateig[1]
rotax = rmeigvec[:,2]

print(rotmat)
print(rotax)
print(np.matmul(rotmat,rotax))