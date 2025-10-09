# py-dmm

[![PyPI version](https://badge.fury.io/py/py-dmm.svg)](https://badge.fury.io/py/py-dmm)
[![Python Support](https://img.shields.io/pypi/pyversions/py-dmm.svg)](https://pypi.org/project/py-dmm/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A Python client library for the DMM (Digital Media Mart) API with full type hints support.

## Features

- 🔍 **Product Search**: Search for products with various filters and parameters
- 📦 **Product Details**: Retrieve detailed information about specific products  
- 🏷️ **Genre/Category Support**: Browse and filter by categories and genres
- 🔒 **Type Safety**: Full type hints support with mypy validation
- ⚡ **Async-Ready**: Built with modern Python practices
- 🧪 **Well Tested**: Comprehensive test suite with pytest
- 📚 **Well Documented**: Complete API documentation and examples

## Installation

Install py-dmm using pip:

```bash
pip install py-dmm
```

For development installation with all optional dependencies:

```bash
pip install py-dmm[dev]
```

## Quick Start

```python
from py_dmm import DMMClient

# Initialize the client with your API key
client = DMMClient(api_key="your_api_key_here")

# Search for products
results = client.search_products(keyword="game", page_size=10)

print(f"Found {results.total_count} products")
for product in results.products:
    print(f"- {product.title} (¥{product.price})")

# Get detailed product information
product = client.get_product("product_id_here")
if product:
    print(f"Product: {product.title}")
    print(f"Description: {product.description}")
    print(f"Price: ¥{product.price}")

# Use as context manager (recommended)
with DMMClient(api_key="your_api_key_here") as client:
    results = client.search_products(keyword="anime")
    # Client will be automatically closed
```

## API Reference

### DMMClient

The main client class for interacting with the DMM API.

#### Constructor

```python
DMMClient(
    api_key: str,
    base_url: str = "https://api.dmm.com/affiliate/v3/",
    timeout: int = 30
)
```

**Parameters:**

- `api_key`: Your DMM API key (required)
- `base_url`: Base URL for the DMM API (optional)
- `timeout`: Request timeout in seconds (optional, default: 30)

#### Methods

##### search_products()

Search for products with various filters.

```python
search_products(
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
    sort: str = "rank",
    **kwargs: Any
) -> SearchResult
```

**Parameters:**

- `keyword`: Search keyword (optional)
- `category`: Product category to filter by (optional)
- `page`: Page number (1-based, default: 1)
- `page_size`: Number of results per page (default: 20)
- `sort`: Sort order - "rank", "price", "date", etc. (default: "rank")
- `**kwargs`: Additional search parameters

**Returns:** `SearchResult` object containing products and pagination info

##### get_product()

Get detailed information about a specific product.

```python
get_product(product_id: str) -> Optional[Product]
```

**Parameters:**

- `product_id`: The ID of the product to retrieve

**Returns:** `Product` object if found, `None` otherwise

##### get_genres()

Get available genres/categories.

```python
get_genres(floor: Optional[str] = None) -> List[Dict[str, Any]]
```

**Parameters:**

- `floor`: Specific floor/service to get genres for (optional)

**Returns:** List of genre dictionaries

### Data Models

#### Product

Represents a product from the DMM API.

```python
@dataclass
class Product:
    product_id: str
    title: str
    description: Optional[str] = None
    price: Optional[float] = None
    currency: str = "JPY"
    image_url: Optional[str] = None
    category: Optional[str] = None
    release_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    rating: Optional[float] = None
```

#### SearchResult

Represents search results from the DMM API.

```python
@dataclass
class SearchResult:
    products: List[Product]
    total_count: int
    page: int = 1
    page_size: int = 20
    total_pages: int = 1
```

### Exception Handling

The library provides specific exception types for different error scenarios:

```python
from py_dmm import DMMError, DMMAPIError, DMMAuthError

try:
    client = DMMClient(api_key="invalid_key")
    results = client.search_products(keyword="test")
except DMMAuthError as e:
    print(f"Authentication failed: {e}")
except DMMAPIError as e:
    print(f"API error: {e} (Status: {e.status_code})")
except DMMError as e:
    print(f"General error: {e}")
```

## Configuration

### Environment Variables

You can set your API key using an environment variable:

```bash
export DMM_API_KEY="your_api_key_here"
```

Then use it in your code:

```python
import os
from py_dmm import DMMClient

api_key = os.getenv("DMM_API_KEY")
client = DMMClient(api_key=api_key)
```

### API Key

To use this library, you need a DMM API key. You can obtain one by:

1. Visiting the [DMM Affiliate Program](https://affiliate.dmm.com/)
2. Registering for an account
3. Generating an API key from your dashboard

## Development

### Setup Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/richardnguyen99/py-dmm.git
   cd py-dmm
   ```

2. Install development dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=py_dmm

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Quality

The project uses several tools to maintain code quality:

```bash
# Format code with black
black py_dmm tests

# Sort imports with isort  
isort py_dmm tests

# Type checking with mypy
mypy py_dmm

# Linting with pylint
pylint py_dmm
```

### Building and Publishing

```bash
# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to:

1. Update tests as appropriate
2. Follow the existing code style (black + isort)
3. Add type hints to new code
4. Update documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Support

- 📖 [Documentation](https://py-dmm.readthedocs.io/)
- 🐛 [Issue Tracker](https://github.com/richardnguyen99/py-dmm/issues)
- 💬 [Discussions](https://github.com/richardnguyen99/py-dmm/discussions)

## Related Projects

- [DMM API Documentation](https://affiliate.dmm.com/api/)
- [DMM Affiliate Program](https://affiliate.dmm.com/)

---

Made with ❤️ by [Richard Nguyen](https://github.com/richardnguyen99)
