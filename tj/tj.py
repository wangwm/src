# code for python3
from itertools import groupby
import numpy as np

lst= [
    2648, 2648, 2648, 63370, 63370, 425, 425, 120,
    120, 217, 217, 189, 189, 128, 128, 115, 115, 197,
    19752, 152, 152, 275, 275, 1716, 1716, 131, 131,
    98, 98, 138, 138, 277, 277, 849, 302, 152, 1571,
    68, 68, 102, 102, 92, 92, 146, 146, 155, 155,
    9181, 9181, 474, 449, 98, 98, 59, 59, 295, 101, 5
]
lst2=[]
fh = open('./aa3.txt')
for line in fh.readlines():
    lst2.append(float(line) *1)

len2 = len(lst2)
print len2

#for k, g in groupby(sorted(lst), key=lambda x: x//50):
#    print('{}-{}: {}'.format(k*50, (k+1)*50-1, len(list(g))))
v_step=0.005
ZERO_FLOAT = 0.00000001
#for k, g in groupby(sorted(lst2), key=lambda x: x//v_step):
#    print('{}-{}: {}'.format(k*v_step, (k+1)*v_step, float(100*len(list(g))/len2)))

def get_section(data,total_sec_num, v_step = 0.005):
    out =[]
    
    var_total =100
    left_sec_num =total_sec_num
    each_sect_var = var_total/left_sec_num

    len_total = len(data)
    sect_var = 0
    mink =  0;
    maxk =  0;
    
    
    for k, g in groupby(sorted(lst2), key=lambda x: x//v_step):
        maxk =  (k+1)*v_step;
        
        tmp = float(100*len(list(g)))
        sect_var += np.round(tmp/len_total,5) 

           
        if sect_var >each_sect_var and left_sec_num>ZERO_FLOAT :
            o={}
            o['mink'] =  np.round(mink,3)
            o['maxk'] =  np.round(maxk,3)
            o['var'] =   np.round(sect_var,3)
            out.append(o)
            
            var_total -= sect_var
            left_sec_num -= 1
            if left_sec_num > ZERO_FLOAT: #next
                each_sect_var = var_total/left_sec_num
                        
            sect_var = 0
            mink =  maxk;
    print left_sec_num, sect_var,mink,maxk         
    if sect_var> ZERO_FLOAT: 
        o={}
        o['mink'] =  np.round(mink,3)
        o['maxk'] =  1
        o['var'] =   np.round(sect_var,3)
        out.append(o)
        
    return out
      
t = 0      
o =  get_section(lst2,5,0.0005)  
print o
for k in o:
    t+=k['var']
print t    
