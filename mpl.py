from re import X
import matplotlib.pyplot as plt
import numpy as np
fig, ax = plt.subplots()

def rotate(x,y, alpha):
    rho = np.sqrt((x*x)+(y*y))
    cosphi = x/rho
    sinphi = y/rho 
    newx = ((np.cos(alpha)*cosphi)-(np.sin(alpha)*sinphi))*rho
    newy = ((np.sin(alpha)*cosphi)+(np.cos(alpha)*sinphi))*rho
    return newx, newy

alpha = float(input())/(180/np.pi)
n = int(input())

for i in range(n):
    x=float(input())
    y=float(input())
    plt.scatter(x,y, color="red")
    newx, newy = rotate(x,y,alpha)
    ax.plot([0,newx],[0,newy])
    ax.plot([0,x],[0,y])
    plt.scatter(newx,newy,color="blue")
    xi=x 
    yi=y
    for i in range(100):
        tempx,tempy=rotate(xi,yi,alpha/100)
        ax.plot([xi,tempx],[yi,tempy],color="black")
        xi=tempx 
        yi=tempy

plt.xlim(-10,10)
plt.ylim(-10,10)
plt.show()