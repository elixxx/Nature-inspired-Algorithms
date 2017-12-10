class MarketType():

    def __init__(self, max_price, max_demand):
        self._max_price = max_price
        self._max_demand = max_demand

    def demand(self, price):
        #if price is greater than max price, return 0
        if price > self._max_price:
            return 0

        #if product is free return max_demand (ignore negative price)
        if price <= 0:
            return self._max_demand

        #else determine demand based on price
        #How does this formula work?
        demand = self._max_demand - price**2 * self._max_demand / self._max_price**2

        return demand

    @property
    def max_price(self):
        return self._max_price

    @property
    def max_demand(self):
        return self._max_demand