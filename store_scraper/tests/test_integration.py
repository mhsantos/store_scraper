import json
import pytest
import requests

from unittest import TestCase

"""
Makes an actual call to the /aptoide endpoint to make sure that it returns valid details
about the requested app.

Unlike a unit test, this is not expected to validate if the code is running, but actually
the integration between the game_scraper and Aptoide.

This could be used in conjunction with a /_health endpoint to validate if:
1. game_scraper can submit requests and get responses from aptoide.com
2. game_scraper is up and running
3. the AptoideService scraper is still up to date with the Aptoide html structure
"""


@pytest.mark.skip(reason="only run when local falcon app is running")
class AptoideIntegrationTest(TestCase):
    def test_get_app_details(self):
        details_response = requests.get(
            "http://localhost:8000/aptoide?search=https://lords-mobile.en.aptoide.com/app"
        )
        assert details_response.status_code == 200
        app_details = json.loads(details_response.text)
        assert app_details["name"] == "Lords Mobile"
