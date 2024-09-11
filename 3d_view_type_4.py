
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

vt = 6000
ht = 5000
build_up = 2
sur_co = np.array([15.32, 5.06])

azi = 1.0472
r = 18000/(3.14*build_up)

r = math.ceil(r)
kop = vt - r
hx = ht - r

e = []
n = []
d = []
e1 = []
n1 = []
d1 = []
h = []


#Vertical drilling
ditr = 0
eitr = sur_co[1]
nitr = sur_co[0]
for i in range(kop):
    d.append(ditr)
    e.append(eitr)
    n.append(nitr)
    ditr += 1


#Build Section

for i in range(r):
  d.append(ditr)
  ditr += 1
  x = math.asin(i/r)
  hitr = r - r*math.cos(x)
  h.append(hitr)
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)
  e1.append(eitr)
  n1.append(nitr)
  d1.append(ditr)
  

# Horizontal Drilling
for k in range(hx):
  d.append(ditr)
  hitr += 1
  h.append(hitr)
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)


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

df.to_csv('type_4.csv', index=False)