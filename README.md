# bricklink_py
###### Version: 0.1.0
---
This Python library provides a convenient wrapper for interacting with the Bricklink API. Bricklink is an online marketplace for buying and selling LEGO® bricks, sets, and minifigures.

With this wrapper, you can easily integrate Bricklink's functionality into your Python applications, allowing you to perform various operations such as searching for items, retrieving store inventories, managing orders, and more. It abstracts away the complexities of the API, providing a simple and intuitive interface.

### Key Features

- *Item Search*: Search for items on Bricklink using various criteria like keywords, category, color, and more.
- *Store Inventory*: Retrieve store inventories, including available quantities and prices.
- *Order Management*: Create, update, and retrieve order information, including order status, items, and shipping details.
- *Catalog Information*: Access detailed information about LEGO® items, including their categories, colors, and images.
- *Price Guide*: Get pricing information for items based on condition and quantity.
- *Authentication*: Provides methods to obtain and manage the necessary API tokens for authenticating requests.

### Installation

```bash
$ pip install bricklink-py
```

```python
from bricklink_py import bricklink

session = bricklink.Bricklink('credentials')
```

### Example

```python
from html import unescape
from bricklink_py import bricklink

# create session object
    session = bricklink.Bricklink(
    consumer_key='your_consumer_key',
    consumer_secret='your_consumer_secret',
    token='your_token',
    token_secret='your_token_secret'
)

# Price checker example
set_no = '75281-1'

set_item = session.catalog_item.get_item('SET', set_no)
set_name = unescape(set_item['name'])
set_weight = set_item['weight']
year_released = set_item['year_released']

price_guide = session.catalog_item.get_price_guide('SET', set_no,
                                                   guide_type='sold')
avg_price = float(price_guide['avg_price'])
currency = price_guide['currency_code']

print(f'The "{set_name}" set was released in {year_released}.')
print(f'It weights {set_weight}gr.')
print(f'Average sold price for last 6 months: {avg_price:.2f} {currency}')
```
Output:
```
>> The "Anakin's Jedi Interceptor" set was released in 2020.
>> It weights 360.00gr.
>> Average sold price for last 6 months: 41.27 EUR
```

### Getting Bricklink API Credentials

To use the Bricklink API, you need to obtain API tokens from the Bricklink API consumer page. Here's how you can get started:

1. Visit the [Bricklink API page](https://www.bricklink.com/v2/api/welcome.page).
2. Agree the [API Terms of Use](https://www.bricklink.com/v3/terms_of_use_api.page) to use BrickLink API.
3. Login/Register in the [consumer page](https://www.bricklink.com/v2/api/register_consumer.page)
4. Generate an access token with your external IP.
5. Then you have all the credentials needed for the session object.

### Contributions and Issues

Contributions, bug reports, and feature requests are welcome! If you encounter any issues or have any suggestions, please create an issue on the GitHub repository.

### License

This project is licensed under the GNU Affero General Public License (AGPL). Feel free to use, modify, and distribute it according to the terms of the AGPL license.

LEGO® is a trademark of the LEGO Group of companies, which does not sponsor, authorize, or endorse this project.
