# App store scraper

This is a simple API written in python and served by the [Falcon](https://falconframework.org/) web API framework.

The API has only one endpoint `/aptoide?search={aptoide_app_url}` that takes a valid Aptoid app store URL and fetches the information for the given app URL.

Internally, the scraper uses the [Beautiful Soup library](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to parse and navigate through the page structure to get the app details.

## /aptoide

The `/aptoide` endpoint takes a single query string parameter named `search`. The `search` parameter must be a valid Aptoide app page url: `https://<app-name>.en.aptoide.com/app`, where `app-name` is composed only by alphanumeric characters or `-`.

Examples of valid URLs:

https://ubereats.en.aptoide.com/app  
https://lords-mobile.en.aptoide.com/app  
https://defend-the-earth.en.aptoide.com/app

The endpoint returns a json with the following information:

```
{
  "name": "App Name",
  "version": "2.104",
  "downloads": "7.5M",
  "release_date": "28-04-2023",
  "description": "App description"
}
```

## Setup
To install the required libraries, from the repository root, run:
```
pip install -r requirements.txt
```

## Running the application
From inside the `store_scraper` folder, run:
```
gunicorn -w 2 'app:get_app()'
```

## Testing
From a separate terminal, run:
```
curl -v "http://localhost:8000/aptoide?search=https://<app-name>.aptoide.com/app"
```

## Unit tests
From the store_scraper folder, run:
```
python -m pytest tests 
```

## Future work
There is an integration test in `store_scraper/tests/test_integration.py`. That test submits an actual request to the API and parses the result.
It could be used later for a health check endpoint and alert if the page structure changes, rendering the parser invalid.

There is also a Dockerfile to create an app image that can be deployed to a public cloud for running the service.
