from amazon.api import AmazonAPI, AsinNotFound

amazon = AmazonAPI("AKIAJ4DKCCVFZIVIHWHA", "rYYuJf3c5maYOnDM2EBNd+d5sJWgXGsphgLR2Y7a", "literapy-21")

try:
	products = amazon.lookup(SearchIndex='All', IdType='ISBN', ItemId='9780450040184')

	print(products[0].offer_url)
except AsinNotFound:
	print('No Result')
