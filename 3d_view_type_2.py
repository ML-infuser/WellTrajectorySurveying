import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

vt = 12000
ht = 6000
kop = 1500
build_up = 2
drop_off = 1.5
eoc = 11000
f_inc = 0.349066
azi = 1.0472

sur_co = np.array([15.32, 5.06])

r1 = 18000/(3.14*build_up)
r2 = 18000/(3.14*drop_off)

oq = ht - r1 - r2*math.cos(f_inc) - (vt - eoc)*math.tan(f_inc)
op = eoc - kop + r2*math.sin(f_inc)
qs = r1 + r2
pq = (op**2 + oq**2)**0.5
ps = (pq**2 - qs**2)**0.5
x = math.atan(oq/op)
y = math.atan(qs/ps)
alpha = x + y
# print(alpha)

vc = r1*math.sin(alpha)
vc = math.ceil(vc)
vd = ps*math.cos(alpha)
vd = math.ceil(vd)
ve = eoc - vd - vc - kop
v5 = ve + r2*math.sin(f_inc)
v5 = math.ceil(v5)
vf = vt - eoc


e = []
n = []
d = []
e1 = []
n1 = []
d1 = []
e2 = []
n2 = []
d2 = []
h = []


eitr = sur_co[1]
nitr = sur_co[0]
ditr = 0
#vertical drilling
for i in range(kop +1):
  n.append(nitr)
  e.append(eitr)
  d.append(ditr)
  ditr += 1


#build up
for i in range(1,vc+1):
  ditr += 1
  d.append(ditr)
  beta = math.asin(i / r1)
  hitr = r1 - i/(math.tan(beta))
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


#hold
for i in range(1,vd+1):
  ditr += 1
  d.append(ditr)
  hitr = i*math.tan(alpha) + r1*(1 - math.cos(alpha))
  h.append(hitr)
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)
  
  
#drop
hd = h[-1]
gamma = 0
p5 = 0
for i in range(1,ve+1):
  ditr += 1
  d.append(ditr)
  p5 = v5 - i
  gamma = math.asin(p5/r2)
  hitr = r2*math.cos(gamma) - r2*math.cos(alpha) + hd
  h.append(hitr)
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)
  e2.append(eitr)
  n2.append(nitr)
  d2.append(ditr)

  

#hold
he = h[-1]
for i in range(1 , vf+1):
  ditr += 1
  d.append(ditr)
  hitr = he + i*math.tan(f_inc)
  h.append(hitr)
  eitr = hitr*math.cos(azi)
  nitr = hitr*math.sin(azi)
  eitr = eitr + sur_co[1]
  nitr = nitr + sur_co[0]
  e.append(eitr)
  n.append(nitr)

ax = plt.axes(projection = '3d')
ax.plot(e,n,d)
ax.plot(e1,n1,d1,color = 'k')
ax.plot(e2,n2,d2,color = 'k')
plt.xlabel("East")
plt.ylabel("North")
ax.set_zlabel('Depth')
ay = plt.gca()
ay.invert_zaxis()
# plt.show()

import pandas as pd
data = {
    'n': n,
    'e': e,
    'd': d
}

df = pd.DataFrame(data)

df.to_csv('type_2.csv', index=False)