import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd

vt = 9880
kop = 1650
sur_co = np.array([15.32, 5.06])
tar_co = np.array([1650, 4510])
build_up = 1.5

d = []
h = []

r = 18000/(3.14*build_up)
a=0
for [t_cor,s_cor] in zip(tar_co,sur_co):
  a += (t_cor-s_cor)**2
a=np.sqrt(a)
ht = a
# plt.plot(5.06,15.32,marker = "*")
# plt.show()

# Measured depth
x = 0
y = 0
x = math.atan((ht-r)/(vt - kop))
y = math.asin(r/((1/math.cos(x)) * (vt-kop)))
alpha = x + y
# print(alpha)

vc = r*math.sin(alpha)

azi = math.atan((tar_co[0] - sur_co[0])/(tar_co[1] - sur_co[1]))

e = []
n = []
d = []

e1 = []
n1 = []
d1 = []


#for vertical section
eitr = sur_co[1]
nitr = sur_co[0]
ditr = 0
for i in range(kop +1):
    e.append(eitr)
    n.append(nitr)
    d.append(ditr)
    ditr += 1
 
# for build section
vc = math.ceil(vc)

for i in range(1,vc+1):
  beta = math.asin(i / r)

  ditr += 1
  d.append(ditr)
  hitr = r - i*(1/math.tan(beta))
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
   

# hold profile
vd = 0
hx = 0
for k in range(vt-kop-vc):
  vd = vt - kop - vc -k
  hx = ht - vd /(math.tan(1.570796 - alpha))
  ditr += 1
  d.append(ditr)
  h.append(hx)
  eitr = hx*math.cos(azi)
  nitr = hx*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)

# print(d[-1])
# ax = plt.axes(projection = '3d')
# ax.plot(e,n,d, color = 'c')
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

df.to_csv('type_1.csv', index=False)
