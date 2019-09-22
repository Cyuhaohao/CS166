import random
from scipy.stats import norm
import matplotlib.pyplot as plt


def f(x):
    Z = 24.44321494051954
    if abs(x) > 7:
        return 0
    elif abs(x) > 3:
        return 3*(1-(x/7)**2)**0.5/Z
    elif abs(x) > 1:
        return ((3-abs(x))/2-3/7*10**0.5*((3-x**2+2*abs(x))**0.5-2))/Z
    elif abs(x) > 0.75:
        return (9-8*abs(x))/Z
    elif abs(x) > 0.5:
        return (3 * abs(x) + 0.75) / Z
    else:
        return 2.25/Z


T = 100000
sigma = 1
thetamin = -8
thetamax = 8
theta = [0.0] * (T + 1)
print(theta)
theta[0] = random.uniform(thetamin, thetamax)

t = 0
while t < T:
    t = t + 1

    theta_star = norm.rvs(loc=theta[t - 1], scale=sigma, size=1, random_state=None)  # 从已知正态分布q中生成候选状态

    alpha = min(1, (f(theta_star[0])/f(theta[t - 1])))

    u = random.uniform(0, 2)
    if u <= alpha:
        theta[t] = theta_star[0]
    else:
        theta[t] = theta[t - 1]

# print (theta)
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)
plt.sca(ax1)
plt.ylim(thetamin, thetamax)
plt.plot(range(T + 1), theta, 'g-')
plt.sca(ax2)
num_bins = 100
plt.hist(theta, num_bins, normed=1, facecolor='red', alpha=0.5)
plt.show()