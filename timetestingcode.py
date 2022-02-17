#from sense_hat import SenseHat
import pandas as pd
import numpy as np
import datetime as dt

N=1000000

#sense = SenseHat()
data = pd.DataFrame({"ts": np.zeros((N,)), 
                     "roll": np.zeros((N,)),
                     "pitch": np.zeros((N,)),
                     "yaw": np.zeros((N,))
                     })

for i in range(N):
    t =  dt.datetime.now().time()
    pitch,roll,yaw = np.random.random(3)
    data.loc[i,:] = [t,pitch,roll,yaw]
    if (i%10000==0):
        print(dt.datetime.now().time(), i)

print(dt.datetime.now().time(), "Writing pickle...")
data.to_pickle("data/datalog.zip")
print(dt.datetime.now().time(), "Writing csv...")
data.to_csv("data/datacsv.csv")
print(dt.datetime.now().time(), "all done.")
