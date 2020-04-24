#coding:utf-8
import sys
import os 
import json

from itertools import groupby
import pandas as pd
import talib 
import numpy as np


ZERO_FLOAT = 0.00000001


######################
out_file ="./high_low_section.json"
g_map ={}

'''
data 输入序列
total_sec_num  划分几个大段落（总100%）
v_min 起步最大 比如-1
v_max  起步最大 比如1
v_step 步长

out_high = get_section(high,5,-1,1,0.0005) 
'''
def get_section(data,total_sec_num=5,v_min=0,v_max=1, v_step = 0.005):
    out =[]
    
    var_total =100
    left_sec_num =total_sec_num
    each_sect_var = var_total/left_sec_num

    len_total = len(data)
    sect_var = 0
    mink =  v_min;
    maxk =  v_max;
        
    for k, g in groupby(sorted(data), key=lambda x: x//v_step):
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
    if sect_var> ZERO_FLOAT: 
        o={}
        o['mink'] =  np.round(mink,3)
        o['maxk'] =  v_max
        o['var'] =   np.round(sect_var,3)
        out.append(o)
        
    return out
    
 
def walkFile(file):                                  
    for root, dirs, files in os.walk(file):               
                                               
        # root 表示当前正在访问的文件夹路径                             
        # dirs 表示该文件夹下的子目录名list                           
        # files 表示该文件夹下的文件list                            
                                                   
        # 遍历文件                                            
        for f in files:
            srcPath = os.path.join(root, f)       
            #print srcPath           
            dat = pd.read_csv(srcPath)
            high = dat["label_1"]
            low = dat["label_2"]
            
            out_high = get_section(high,5,-1,1,0.0005) 
            out_low = get_section(low,5,-1,1,0.0005) 
            code=  f.split(".")[0]
            if g_map.has_key(code):
                continue
            print code    
            g_map[code] ={}
            g_map[code]['high'] = out_high
            g_map[code]['low'] = out_low
            
        # 遍历所有的文件夹                                        
        #for d in dirs:                                    
        #    print(os.path.join(root, d))                  

    strDict = json.dumps(g_map)
    with open(out_file,'w')as f:
        f.write(strDict)

if __name__ == '__main__':
    #wine = pd.read_csv("sz002464.csv")
    #wine.head()
    #print "----------------------------"
    #convert(wine.head(178).tail(5))
    walkFile("./converted_data/")
