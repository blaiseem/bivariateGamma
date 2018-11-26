import scipy
import scipy.stats
import numpy as np

def costFunction(guess, params):
    """Function used to optimise parameters in sample generation.

    Parameters
    ----------
    guess: list
        List of 3 values used as H1, H2 and gamma respectively in this script.
        Must all be > 0.
        Must also be such that delta1 and delta2 > 0 too.
    params: list
        List of 6 objects.
            alpha1, alpha2: floats
            rho: float
            wu: weights to use in gauss legendre integration of inverse gamma distribution function
            xu, xv: x values to use in gauss legendre integration of inverse gamma distribution function
            a, b: limits of gauss legendre integration. Normally 0 and 1 respectively
    
    Returns
    ----------
    F: float
        function returns 0 when guess is correct. F represents absolute error
    """
    alpha1, alpha2, rho, wu, xu, xv, a, b = params
    H1 = guess[0]
    H2 = guess[1]
    gamma = guess[2]
    delta1 = alpha1-H1-gamma
    delta2 = alpha2-H2-gamma
    if (H1<0) or (H2<0) or (gamma<0) or (delta1<0) or (delta2<0):
        F   = 1e+6
    else:
        if rho >= 0:
            x1 = xu
            x2 = xv
        else:
            x1 = 1-xu
            x2 = 1-xv
        
        #EV represents gauss legendre integration of inverse cumulative normal distribution functions multiplied together.
        EV = sum(
            scipy.stats.gamma.ppf(x1, H1, scale=1) * scipy.stats.gamma.ppf(x2, H2, scale=1) * wu
        )*0.5*(b-a)
        
        F = abs(
            (EV - H1*H2 + gamma) / np.sqrt(alpha1*alpha2) - rho
        )
        

    return F

def generateSamples(mu=[1,1],sigma=[1,1],rho=0,size=10000,glPoints=25):
    """Function used to generate correlated bivariate gamma variables given mean, standard deviation of each and correlation

    Parameters
    ----------
    mu: list
        List of the means of two variables
    sigma: list
        List of the standard deviation of the two variables
    rho: float
        Correlation between both random variables
    size: integer
        Number of sampels to generate
    glPoints: integer
        Number of points to use in gausse legendre integration.
        Literature suggests 25 points provide a good balance in accuracy and speed.
    
    Returns
    ----------
    X: list
        List containing 2 elements.
        Each is an array of length size.
        The mean and standard deviation should match the specified inputs.
        The correlation between the elements should match the input correlation.
    
    """
    #converting mean and standard deviation to theta and k values.
    #assumes gamma distribution of the form f(x) = (1/(Gamma(k)*theta^k))*x^(k-1)*exp(-x/theta)
    theta = [
        (sigma[0]**2)/mu[0],
        (sigma[1]**2)/mu[1]
    ]
    
    k = [
        mu[0]/theta[0],
        mu[1]/theta[1]
    ]
    
    
    #generating gauss legendre integration params
    b, a = 1, 0
    xu, wu = np.polynomial.legendre.leggauss(glPoints)
    xu = 0.5*(xu + 1)*(b - a) + a
    if rho >= 0:
        xv = xu
    else:
        xv = (1-xu)

    #initial guess
    H = [k[0]/3, k[1]/3]
    gamma = min(H)
    x0 = [H[0], H[1], gamma]

    #optimise params
    paramsOptimisation = scipy.optimize.minimize(
        fun = costFunction,
        x0 = x0,
        args = [k[0],k[1],rho,wu,xu,xv,a,b],
        tol = 1e-12,
        method = 'Nelder-Mead'
    )
    
    optimalParams = paramsOptimisation.x

    #store optimal params
    H[0] = optimalParams[0]
    H[1] = optimalParams[1]
    gamma = optimalParams[2]
    delta = [
        k[0]-H[0]-gamma, 
        k[1]-H[1]-gamma
    ]

    #generate uniform random variables
    U = np.random.uniform(size=size)
    Uz = np.random.uniform(size=size)
    Uw1 = np.random.uniform(size=size)
    Uw2 = np.random.uniform(size=size)
    
    if rho >= 0:
        V = U
    else:
        V = 1 - U

    #generate intermediate gamma variables
    TU = scipy.stats.gamma.ppf(U, H[0], scale=1)
    TV = scipy.stats.gamma.ppf(V, H[1], scale=1)
    Z = scipy.stats.gamma.ppf(Uz, gamma, scale=1)
    W1 = scipy.stats.gamma.ppf(Uw1, delta[0], scale=1)
    W2 = scipy.stats.gamma.ppf(Uw2, delta[1], scale=1)

    #generate final gamma variables
    X = [((TU + Z + W1)*theta[0]), ((TV + Z + W2)*theta[1])]

    return X