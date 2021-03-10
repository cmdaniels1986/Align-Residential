prices = 'Studio, 1 Bath Apartment #204 at Fifteen Fifty'

start =prices.find('#')
finish = prices.find(' at ')

print(prices[start:finish].replace('#','').strip())
