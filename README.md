# Bricklink API Python Wrapper

This Python library provides a clean wrapper for the Bricklink API, making it simple to integrate Bricklink's marketplace functionality into your Python projects. Access item searches, inventory management, order processing, and more through an intuitive interface that handles all the API complexities behind the scenes.

## Key Features

- **Item Search** - Find Bricklink items using filters for keywords, categories, colors, and more
- **Store Inventory** - Access store inventories with current quantities and pricing
- **Order Management** - Handle order creation, updates, and tracking
- **Catalog Information** - Get detailed item data including categories and images
- **Price Guide** - Access current market pricing based on condition and quantity
- **Authentication** - Simplified token management for API access

## Installation
##### Install pre-release version
```bash
pip install bricklink-py --pre
```

## Quick Start

```python
from bricklink_py import Bricklink

session = Bricklink('your_credentials')
```

## Example Usage

```python
from html import unescape
from bricklink_py import Bricklink

# Initialize API session
session = Bricklink(
    consumer_key='your_consumer_key',
    consumer_secret='your_consumer_secret',
    token='your_token',
    token_secret='your_token_secret'
)

# Check pricing for a specific set
set_no = '75281-1'

# Get basic set information
set_item = session.catalog_item.get_item('SET', set_no)
set_name = unescape(set_item['name'])
set_weight = set_item['weight']
year_released = set_item['year_released']

# Get pricing data
price_guide = session.catalog_item.get_price_guide('SET', set_no, guide_type='sold')
avg_price = float(price_guide['avg_price'])
currency = price_guide['currency_code']

print(f'The "{set_name}" set was released in {year_released}.')
print(f'It weighs {set_weight}g.')
print(f'Average sold price for last 6 months: {avg_price:.2f} {currency}')
```

Output:
```
The "Anakin's Jedi Interceptor" set was released in 2020.
It weighs 360.00g.
Average sold price for last 6 months: 41.27 EUR
```

## Getting API Credentials

To use the wrapper, you'll need Bricklink API credentials:

1. Visit the [Bricklink API page](https://www.bricklink.com/v2/api/welcome.page)
2. Accept the [API Terms of Use](https://www.bricklink.com/v3/terms_of_use_api.page)
3. Sign in or register on the [consumer page](https://www.bricklink.com/v2/api/register_consumer.page)
4. Generate an access token with your external IP
5. Use the provided credentials in your session object

## Contributing

Contributions, bug reports, and feature requests are welcome! If you find issues or have ideas for improvements, please open an issue on GitHub.

## License

This project is licensed under the GNU Affero General Public License (AGPL).

---

LEGO® is a trademark of the LEGO Group, which does not sponsor, authorize, or endorse this project.
