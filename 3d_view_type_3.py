import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

ht = 1500
vt = 10000
kop = 7000
sur_co = np.array([5.06,15.32])
azi = 1.0472

h = []
e = []
n = []
d = []
e1 = []
n1 = []
d1 = []

p = vt - kop
alpha = 2*math.atan(ht/(vt-kop))
r = (vt - kop)/math.sin(alpha)

ditr = 0
hitr = 0
eitr = sur_co[1]
nitr = sur_co[0]

#Vertical drilling
for i in range(kop):
    e.append(eitr)
    n.append(nitr)
    d.append(ditr)
    ditr += 1

#Build section
for i in range(p):
  x = math.asin(i/r)
  hitr = r - r*math.cos(x)
  h.append(hitr)
  d.append(ditr)
  ditr += 1
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)
  
  e1.append(eitr)
  n1.append(nitr)
  d1.append(ditr)

# ax = plt.axes(projection = '3d')
# ax.plot(e,n,d)
# ax.plot(e1,n1,d1,color = 'k')
# plt.xlabel("East")
# plt.ylabel("North")
# ax.set_zlabel('Depth')
# ay = plt.gca()
# ay.invert_zaxis()
# plt.show()

import pandas as pd
data = {
    'n': n,
    'e': e,
    'd': d
}

df = pd.DataFrame(data)

df.to_csv('type_3.csv', index=False)