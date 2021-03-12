address = ''Mission Fifteen Fifty: Jr. 1 Bedroom, 1 Bath'

street = address[0:address.find('  ')].strip()
city = address.replace(street,'').strip()
city = city[0:city.find(',')].strip()
state = address[address.find(',')+1:address.rfind(' ')].strip()
# state = address.rfind(' ')
print(state)
