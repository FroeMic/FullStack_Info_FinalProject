from app import app, queue, db
from amazon.api import AmazonAPI, AsinNotFound

amazon = AmazonAPI(app.config['AMAZON_ACCESS_KEY'], app.config['AMAZON_SECRET_KEY'], app.config['AMAZON_ASSOC_TAG'])

try:
	products = amazon.lookup(SearchIndex='All', IdType='ISBN', ItemId='9780450040184')

	print(products[0].offer_url)
except AsinNotFound:
	print('No Result')
