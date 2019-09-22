import pandas
from scipy.optimize import minimize
import numpy as np

pa_data=pandas.read_csv('proctatinium_data.csv')

# print(pa_data['time'])

def left_pa(l):
    sum_abs=0
    for i in range(1,83):
        sum_abs+=(abs(32*np.e**(-l*pa_data['time'][i])-(pa_data['count_rate'][i]+np.random.normal(0,1))))
        print((abs(32*np.e**(-l*pa_data['time'][i])),(pa_data['count_rate'][i]+np.random.normal(0,1))))
    return sum_abs

def func():
    v=lambda l: left_pa(l)
    return v

l0 = np.asarray((1))
res=minimize(func(),l0)

print(res.fun)
print(res.success)
print(res.x)

