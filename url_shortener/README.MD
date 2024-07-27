# URL Shortener

This Python script allows you to shorten URLs using the is.gd API. You can specify a custom alias for the shortened URL.

## Features

- Shortens URLs using the [is.gd](https://is.gd/) API.
- Optionally allows for custom aliasing of shortened URLs.
- Simple and easy to use.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone this repository or download the script.

2. Ensure you have Python 3.x installed on your system.

3. Install the required Python package:

    ```bash
    pip install requests
    ```

## Usage
Define the original URL you want to shorten and an optional custom alias.

Call the url_shortener function with the original URL and custom alias.

The function will return the shortened URL if successful, or print an error message if not.

## Notes
The url_shortener function uses the requests library to make HTTP GET requests to the is.gd API.

The nick_url parameter allows for specifying a custom alias for the shortened URL. 

**If the alias is already taken, the API will return an error.**


## Acknowledgments

- The [is.gd](https://is.gd/) service for providing the URL shortening API.