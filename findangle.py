import numpy as np
import datetime as dt
import pandas as pd
from logzero import logger,logfile
#from orbit import ISS

#TODO ORBIT LIBRARY!!!
#TODO write rpi version

logfile("data/logfile.log")

#division remainder for float
def modfromfloat(num:float, m:float):
    return num-(int(num/m)*m)

#function to simulate roll pitch and yaw in radian sensor reading
def simsensorrpy(r0:float=np.pi, p0:float=0., y0:float=1.5*np.pi):
    tt = dt.datetime.now().microsecond%100
    return {"roll": modfromfloat(r0+tt+np.random.randint(-3,3),2*np.pi),
    "pitch": modfromfloat(p0+tt+np.random.randint(-3,3),2*np.pi),
    "yaw": modfromfloat(y0+tt+np.random.randint(-3,3),2*np.pi)}

#calculate how much each angle changed
def moved(x0:float,y0:float,z0:float,x1:float,y1:float,z1:float):
    nx,ny,nz = (x1-x0,y1-y0,z1-z0)
    return nx,ny,nz

#convert roll pitch yaw to a rotation matrix
#x: roll
#y: pitch
#z: yaw
#returns a 3x3 numpy matrix
def rotmatrix(x: float, y: float, z: float):
    Rx = np.array([[1,0,0],[0,np.cos(x),-np.sin(x)],[0,np.sin(x),np.cos(x)]])
    Ry = np.array([[np.cos(y),0,np.sin(y)],[0,1,0],[-np.sin(y),0,np.cos(y)]])
    Rz = np.array([[np.cos(z),-np.sin(z),0],[np.sin(z),np.cos(z),0],[0,0,1]])
    rotmat=np.matmul(np.matmul(Rz,Ry),Rx)
    return rotmat

#finds axi and angle of rotation given a 3x3 rotation matrix
def findaxisangle(rotmat:np.array):

    #eigenvalues and eignevectors
    rotmateig = np.linalg.eig(rotmat)

    #find which eignevalue is real
    #at least one will be, so j will be defined after this loop
    for i in range(len(rotmateig[0])): #for each eigenvalue
        if np.isreal(rotmateig[0][i]):
            j=i
            break

    rotmateigvec = rotmateig[1]  #matrix of eigenvectors
    rotax = rotmateigvec[:,j] #this is the rotation axis - it corresponds to a real eignevalue=1
    rotax = rotax.real #removes complex part (which would be 0*j)

    v = rotmateig[0][j-1] #takes one of the other eigen values, which will be complex unlex rotmat is identity
    a = np.real(v)
    b = np.imag(v)

    rotan = np.arctan2(b,a)#complex eignevalues will have the form cos(phi) + i sin(phi) so take the arctan2(sin,cos)
    
    return rotax,rotan


#initialize the variables
tstart = dt.datetime.now() #start time
N = 1000 #n of readings to take
i=0 #counter of readings
saveN = 250 #n of readings to save in single save file
tdelta = dt.timedelta(minutes=1) #how much time to run program for
tend = tstart+tdelta #finish time for program

data = pd.DataFrame({"ts": np.full(saveN,-1), 
                     "roll": np.full(saveN,-1),
                     "pitch": np.full(saveN,-1),
                     "yaw": np.full(saveN,-1),
                     "axisX":np.full(saveN,-1),        #reserve space for data storage
                     "axisY":np.full(saveN,-1),
                     "axisZ":np.full(saveN,-1),
                     "angle":np.full(saveN,-1)
                     })

try:
    o = simsensorrpy() #take sensor reading
except Exception as e:
    logger.error(f'{e.__class__.__name__}: {e}')
    o = (0.,0.,0.)
oldroll,oldpitch,oldyaw=o["roll"], o["pitch"], o["yaw"]
done = False
tnow = dt.datetime.now()

logger.info("entering loop...")
while not done:
    try:
        o = simsensorrpy() #take sensor reading
        roll,pitch,yaw=o["roll"], o["pitch"], o["yaw"]
        phi,theta,psi=moved(roll,pitch,yaw,oldroll,oldpitch,oldyaw)
        ax, an = findaxisangle(rotmatrix(phi,theta,psi))
        data.loc[i%saveN,:] = [tnow,roll,pitch,yaw,ax[0],ax[1],ax[2],an] #put data into dataframe
        oldroll,oldpitch,oldyaw = roll,pitch,yaw #save old roll pitch yaw for next step

        if (i+1)%saveN==0: #if time to save file 
            filename = "data/readings{:03d}.zip".format((i+1)//saveN) #save file label
            data.to_pickle(filename)
            data = pd.DataFrame({"ts": np.full(saveN,-1), 
                     "roll": np.full(saveN,-1),
                     "pitch": np.full(saveN,-1),
                     "yaw": np.full(saveN,-1),
                     "axisX":np.full(saveN,-1),        #reserve space for data storage
                     "axisY":np.full(saveN,-1),
                     "axisZ":np.full(saveN,-1),
                     "angle":np.full(saveN,-1)
                     })


            logger.info(f"saved file {filename}")
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}')

    tnow = dt.datetime.now()
    i+=1
    done = (tnow>=tend) or (i>=N) #loop exit condition

if i<N: #if exit was due to time
    data.to_pickle("data/readings{:3d}.zip".format((i//saveN)+1)) #save last readings

logger.info("done.")