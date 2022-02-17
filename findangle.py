import numpy as np
import datetime as dt

def modfromfloat(num,m):
    return num-(int(num/m)*m)

def simsensorpry(r0=np.pi, p0=0., y0=1.5*np.pi):
    tt = dt.datetime.now().microsecond%100
    return {"roll": modfromfloat(r0+tt+np.random.randint(-3,3),2*np.pi),
    "pitch": modfromfloat(p0+tt+np.random.randint(-3,3),2*np.pi),
    "yaw": modfromfloat(y0+tt+np.random.randint(-3,3),2*np.pi)}

def moved(x0,y0,z0,x1,y1,z1):
    nx,ny,nz = x1-x0,y1-y0,z1-z0


phi = np.pi/2
theta = 0
psi = 0

def rotmatrix(x,y,z):
    Rx = np.array([[1,0,0],[0,np.cos(x),-np.sin(x)],[0,np.sin(x),np.cos(x)]])
    Ry = np.array([[np.cos(y),0,np.sin(y)],[0,1,0],[-np.sin(y),0,np.cos(y)]])
    Rz = np.array([[np.cos(z),-np.sin(z),0],[np.sin(z),np.cos(z),0],[0,0,1]])
    rotmat=np.matmul(np.matmul(Rx,Ry),Rz)
    return rotmat

def findaxisangle(rotmat):
    rotmateig = np.linalg.eig(rotmat)

    for i in range(len(rotmateig[0])):
        if np.isreal(rotmateig[0][i]):
            j=i
            break

    rmeigvec = rotmateig[1]
    rotax = rmeigvec[:,2]
    rotax = rotax.real

    v = rotmateig[0][j-1]
    a = np.real(v)
    b = np.imag(v)

    rotan = np.arctan2(b,a)
    
    return rotax,rotan

rotmat = rotmatrix(phi,theta,psi)

rotax,rotan = findaxisangle(rotmat)

print(rotax)
print((180*rotan)/np.pi)