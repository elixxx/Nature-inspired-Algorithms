import numpy as np
import matplotlib.pyplot as plt




price = np.linspace(-0.1, 1, 1000)


def demand(price, max_demand, max_price):
    # if price is greater than max price, return 0
    if price > max_price:
        return 0

    # if product is free return max_demand (ignore negative price)
    if price <= 0:
        return max_demand

    # else determine demand based on price
    # How does this formula work?
    demand = max_demand - price ** 2 * max_demand / max_price ** 2

    return demand

demand1 = [demand(p, 2000000, 0.45) for p in price]
demand2 = [demand(p, 30000000, 0.25) for p in price]
demand3 = [demand(p, 20000000, 0.25) for p in price]


plt.plot(price, demand1)
plt.plot(price, demand2)
plt.plot(price, demand3)


plt.show()
