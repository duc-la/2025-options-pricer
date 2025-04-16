from math import log, sqrt, exp
from scipy.stats import norm

#S is current price
#K is strike price
#T is time to maturity
#sigma is volatility
#r is risk free interest rate
def black_scholes(S, K, T, sigma, r, option_type="call"):
    d1 = (
        log(S / K) + 
        (r + 0.5 * sigma**2) * T 
        ) / ( sigma * sqrt(T) 
        )
     
    d2 = d1 - sigma * sqrt(T)

    if option_type == "call":
        price = S * norm.cdf(d1) - (K * exp( -(r * T) ) * norm.cdf(d2) )
    elif option_type == "put":
        price = (
            (K * exp( -(r * T) ) * norm.cdf(-d2) ) - S * norm.cdf(-d1)
        )
    else:
        raise ValueError("option_type must be 'call' or 'put'")
    
    return price

query = list(map(float, input().split()))

print(query)
print(black_scholes(query[0], query[1], query[2], query[3], query[4], "put"))
#100 100 1 0.2 0.05