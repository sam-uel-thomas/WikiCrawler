# WikiCrawler

WikiCrawler is a Python-based web crawler for Wikipedia. It recursively follows the first non-parenthesized, non-italicized link of every page until it converges on 'Philosophy'. It also tracks and records the number of links followed in each journey.

## Installation

Follow these steps to install and run WikiCrawler:

1. **Clone the repository**

    Use the following command to clone this repository:

    ```
    git clone git@github.com:sam-uel-thomas/WikiCrawler.git
    ```

2. **Navigate to the project directory**

    ```
    cd wikicrawler
    ```

3. **Install the required packages**

    WikiCrawler requires several Python packages. Install them with the following command:

    ```
    pip install -r requirements.txt
    ```

    This command assumes that you have Python and pip installed on your machine. If you don't, you'll need to install them first.

## Usage

To run WikiCrawler, use the following command:

```
python app.py
```

This will start the Flask server. You can then use a tool like Postman to make GET requests to the `/run_spider` endpoint. Include the `start_url` parameter in your request to specify the starting point for the web crawler.

For example, if you're running the server locally on port 5000, you could make a request to `http://localhost:5000/run_spider?start_url=https://en.wikipedia.org/wiki/Web_crawler`.

The server will return a JSON response with a message indicating the number of steps taken to reach 'Philosophy' and a list of the visited links.
