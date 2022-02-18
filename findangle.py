from gettext import find
import numpy as np
import datetime as dt
import pandas as pd
#from orbit import ISS

#func that does % but for float
def modfromfloat(num,m):
    return num-(int(num/m)*m)

#whilst our rpi is out of business, use this for roll pitch yaw sensor sim
def simsensorpry(r0=np.pi, p0=0., y0=1.5*np.pi):
    tt = dt.datetime.now().microsecond%100
    return {"roll": modfromfloat(r0+tt+np.random.randint(-3,3),2*np.pi),
    "pitch": modfromfloat(p0+tt+np.random.randint(-3,3),2*np.pi),
    "yaw": modfromfloat(y0+tt+np.random.randint(-3,3),2*np.pi)}

#calculates how much each angle changed
def moved(x0,y0,z0,x1,y1,z1):
    nx,ny,nz = x1-x0,y1-y0,z1-z0
    return nx,ny,nz

#converts roll pitch yaw into a rotation matrix
def rotmatrix(x,y,z):
    Rx = np.array([[1,0,0],[0,np.cos(x),-np.sin(x)],[0,np.sin(x),np.cos(x)]])
    Ry = np.array([[np.cos(y),0,np.sin(y)],[0,1,0],[-np.sin(y),0,np.cos(y)]])
    Rz = np.array([[np.cos(z),-np.sin(z),0],[np.sin(z),np.cos(z),0],[0,0,1]])
    rotmat=np.matmul(np.matmul(Rz,Ry),Rx)
    return rotmat

#finds axis and angle of rotation from a rotation matrix
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

N = 1000
i=0
tstart = dt.datetime.now()
t = dt.timedelta(minutes=1)
tend = tstart+t

data = pd.DataFrame({"ts": np.zeros((N,)), 
                     "roll": np.zeros((N,)),
                     "pitch": np.zeros((N,)),
                     "yaw": np.zeros((N,)),
                     "axis":np.zeros((N,)),        #reserve space for data storage
                     "angle":np.zeros((N,))
                     })

ox,oy,oz = simsensorpry()
tnow = tstart
while tnow<tend:
    roll,pitch,yaw=simsensorpry()
    phi,theta,psi=moved(roll,pitch,yaw,ox,oy,oz)
    ax, an = findaxisangle(phi,theta,psi)
    data.loc[i,:] = [t,roll,pitch,yaw,ax,an]
    ox,oy,oz = roll,pitch,yaw

print(data)