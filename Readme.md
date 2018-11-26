This package can be used to generate samples from a bivariate gamma distribution where the marginal distributions are gamma and the variables are correlated. 

There are restrictions as to what correlations are allowed given the marginal gammas and these are outlined in the reference below.

The methodology is taken from this journal paper:

Schmeiser, B 1981, 'Bivariate Gamma Random Vectors', Operations Research Society of America, vol. 30, no. 2, pp. 355-374.

To use is pretty simple:

Import bivariateGamma package and scipy.stats for later
```
from bivariateGamma import bivariateGamma
import scipy.stats
```

Define input parameters
```
mu = [10,20] #means are 10 and 20
sigma = [1,2] #standard deviations are 1 and 2
rho = -0.3 #correlation is -0.3
```

Generate correlated bivariate variables
```
X = bivariateGamma.generateSamples(mu=mu,sigma=sigma,rho=rho,size=10000,glPoints=25)
```


Test variabels and make sure mean, standard deviation and correlation match
```
print("First variable mean = {}".format(X[0].mean()))
print("Second variable mean = {}".format(X[1].mean()))
print("First variable standard deviation = {}".format(X[0].std()))
print("Second variable standard deviation = {}".format(X[1].std()))
print("Correlation between variables = {}".format(scipy.stats.pearsonr(X[0],X[1])[0]))
```
```
First variable mean = 10.003453766934586
Second variable mean = 19.988343994378614
First variable standard deviation = 1.0063322760244664
Second variable standard deviation = 2.005589619872354
Correlation between variables = -0.27843931145615525
```

Computing mean and standard deviation of difference (X[0]-X[1]) and sum (X[0]+X[1]) of these variables:
```
print("X[0]-X[1] mean = {}".format((X[0]-X[1]).mean()))
print("X[0]+X[1] mean = {}".format((X[0]+X[1]).mean()))
print("X[0]-X[1] standard deviation = {}".format((X[0]-X[1]).std()))
print("X[0]+X[1] standard deviation = {}".format((X[0]+X[1]).std()))
```
```
X[0]-X[1] mean = -9.984890227444025
X[0]+X[1] mean = 29.991797761313197
X[0]-X[1] standard deviation = 2.4817406568339453
X[0]+X[1] standard deviation = 1.9776632823698908
```

And the theoretical values:
```
print("X[0]-X[1] mean (theory) = {}".format((mu[0] - mu[1])))
print("X[0]+X[1] mean (theory) = {}".format((mu[0]+mu[1])))
print("X[0]-X[1] standard deviation (theory) = {}".format((sigma[0]**2+sigma[1]**2-2*sigma[0]*sigma[1]*rho)**0.5))
print("X[0]+X[1] standard deviation (theory) = {}".format((sigma[0]**2+sigma[1]**2+2*sigma[0]*sigma[1]*rho)**0.5))
```
```
X[0]-X[1] mean (theory) = -10
X[0]+X[1] mean (theory) = 30
X[0]-X[1] standard deviation (theory) = 2.4899799195977463
X[0]+X[1] standard deviation (theory) = 1.9493588689617927
```

Enjoy!