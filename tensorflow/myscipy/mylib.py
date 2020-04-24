#-*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import math
import  traceback

# import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar, exp
from sklearn.preprocessing import MinMaxScaler


pai =np.pi


def gaussian(x, *param):
    return param[0] * np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.))) + \
           param[1] * np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))

def maxminnorm2(dataset):
    dataset = dataset.astype(np.float32)
    sc = MinMaxScaler(feature_range=(0, 1))
    sc.fit(dataset)
    transform_data = sc.transform(dataset)
    return transform_data

def maxminnorm(array):
        array = array.astype(np.float32)
        maxcols=array.max(axis=0)
        mincols=array.min(axis=0)
        data_shape = array.shape
        data_rows = data_shape[0]
        data_cols = data_shape[1]
        t=np.empty((data_rows,data_cols))
        for i in xrange(data_cols):
                t[:,i]=(array[:,i]-mincols[i])/(maxcols[i]-mincols[i])
        return t

seed = 2
class my_scipy:
    def __init__(self):
        self.identity = ""
    	self.ZERO_FLOAT = 0.00001

    def linear_line_func(self,x, *param):
        if param[0] <= self.ZERO_FLOAT:
            return 0
        return x  * param[0] + param[1]

    def quadraticCurve_func(self,x, *param):
        if param[0] <= self.ZERO_FLOAT:
            return 0
        return np.power(x - param[1], 2.) * param[0] + param[2]

    def quadraticCurve(self, seq):
        popt = [0, 0, 0]
        pcov = [100, 100, 100]
        perr = [100, 100, 100]
        try:
	    row_num = len(seq)
	    X_ = ar(range(row_num),dtype = 'float32')
	    X_= X_.reshape((row_num,1))
            x =  maxminnorm(X_)
	    x =np.ravel(x)
		
	    Y_= seq.reshape((row_num,1))
            y =  maxminnorm(Y_)
	    y =np.ravel(y)

            popt, pcov = curve_fit(self.quadraticCurve_func, x, y, p0=[3, 4, 3], maxfev=1000)
            perr = np.sqrt(np.diag(pcov))

	
            #plt.plot(x, seq, 'b+:', label='data')
            #plt.plot(x, my_scipy.__quadraticCurve_func(x, *popt), 'ro:', label='fit')
            #plt.legend()
            #plt.show()	
	except:
    		traceback.print_exc()
        finally:
            if math.isinf(perr[0]) or math.isnan(perr[0]):
                return popt, [100, 100, 100]

            return popt, perr


    def linear_line2(self, seq):
        popt=[0,0,0]
        pcov = [100, 100, 100]
        perr = [100, 100, 100]
        try:
            row_num = len(seq)
            X_ = ar(range(row_num),dtype = 'float32')
            X_= X_.reshape((row_num,1))
            x =  maxminnorm2(X_)
            x =np.ravel(x)
            Y_= seq.reshape((row_num,1))
            y =  maxminnorm2(Y_)
            y =np.ravel(y)

            #z1 = np.polyfit(x, y, 1)  #一次多项式拟合，相当于线性拟
            w,c = np.polyfit(x, y, 1, cov=True)
            #p1 = np.poly1d(w)
            perr = np.sqrt(np.diag(c))
            return w,perr 
        except:
    	    traceback.print_exc()
            return popt, [100, 100, 100]


    def linear_line(self, seq):
        popt=[0,0,0]
        pcov = [100, 100, 100]
        perr = [100, 100, 100]
        try:
            row_num = len(seq)
            X_ = ar(range(row_num),dtype = 'float32')
            X_= X_.reshape((row_num,1))
            x =  maxminnorm2(X_)
            x =np.ravel(x)
            Y_= seq.reshape((row_num,1))
            y =  maxminnorm2(Y_)
            y =np.ravel(y)
            popt, pcov = curve_fit(self.linear_line_func, x, y, p0=[3, 1], maxfev=10000)
            #popt, pcov = curve_fit(self.linear_line_func, x, y, p0=[3, 1], maxfev=10000, bounds=(-1000,[np.inf,np.inf]))
            perr = np.sqrt(np.diag(pcov))
            #print perr
            #print "-------------"
            #print popt
            #print "333-------------"
            #plt.plot(x, seq, 'b+:', label='data')
            #plt.plot(x, my_scipy.__linear_line_func(x, *popt), 'ro:', label='fit')
            #plt.legend()
            #plt.show()
        except:
    	    traceback.print_exc()
        finally:
            if math.isinf(perr[0]) or math.isnan(perr[0]):
                return popt, [100, 100, 100]
            return popt,perr


if __name__=='__main__':

    x = ar(range(10),dtype = 'float32')
    #x = np.linspace(0, 10, 10)
    y = ar([0, 1, 2, 3, 4, 5, 4, 3, 2, 1])
    y = ar([0, 10, 20, 30, 40, 50, 40, 30, 20, 10])
    y = ar([10.01, 9.83, 9.55, 9.23, 8.31, 8.78, 8.92, 9.21, 9.46, 9.98])
    test =  my_scipy()
    print  test.linear_line(y)
    print "==============="
    print  test.linear_line2(y)
