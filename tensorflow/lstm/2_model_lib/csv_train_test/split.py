#coding:utf-8
import sys



import pandas as pd
import numpy as np


filename = "sh600263"


if __name__ == '__main__':
    print  sys.argv 
    if len( sys.argv) <2:
        print "please input csv file,such as sh600263"
    filename = sys.argv[1] 

    dat = pd.read_csv(filename+".csv")
    size = len(dat)
    left = int(1*size/10)

    train = dat[:size-left]
    test = dat[-left:]

    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)
    train.to_csv(filename+"_train.csv",index=False)
    test.to_csv(filename+"_test.csv",index=False)
