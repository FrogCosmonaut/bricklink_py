from html import unescape
from bricklink_py import Bricklink

# create session object
session = Bricklink(
    consumer_key='YOUR_CONSUMER_KEY',
    consumer_secret='YOUR_CONSUMER_SECRET',
    token='YOUR_TOKEN',
    token_secret='YOUR_TOKEN_SECRET'
)


# Get all colors example
color_list = session.color.get_color_list()

for color in color_list:
    color_id = color['color_id']
    color_name = color['color_name']
    print(f'id: {color_id} - {color_name}')


# Price checker example
set_no = '75281-1'

set_item = session.catalog_item.get_item('SET', set_no)
set_name = unescape(set_item['name'])
set_weight = set_item['weight']
year_released = set_item['year_released']

price_guide = session.catalog_item.get_price_guide('SET', set_no, guide_type='sold')
avg_price = float(price_guide['avg_price'])
currency = price_guide['currency_code']

print(f'The "{set_name}" set was released in {year_released}.')
print(f'It weights {set_weight}gr.')
print(f'Average sold price for last 6 months is {avg_price:.2f}{currency}')