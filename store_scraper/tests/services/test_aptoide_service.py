import io
import requests
from unittest import TestCase
from unittest.mock import patch


from services import aptoide_service
from models.app_details import AppDetails


class RequestsResponseMock:
    def __init__(self, text: str, status_code: int):
        self.text = text
        self.status_code = status_code


class AptoideServiceTest(TestCase):
    @patch.object(requests, "get")
    def test_get_page_contents(self, requests_get):
        fake_response_text: str = "<body><title>Mock Page</title></body>"
        requests_get.return_value = RequestsResponseMock(fake_response_text, 200)

        svc = aptoide_service.AptoideService()
        page_contents = svc._get_page_contents("")
        assert page_contents == fake_response_text

    def test_parse_soup(self):
        """
        For this test, we extracted the contents of the Lords Mobile app page and saved it
        to a local html file. This test reads those contents and tries to parse it by
        calling the service _parse_soup() method.
        The contents of the page and the Aptoide page structure may change over time, which
        would render this test useless. The purpose of this test though, is not to attest that
        the parser is up to date with the page structure, but instead, to make sure that future
        Beautiful Soup versions keep working as expected for a payload that we had successfully
        parsed in the past.

        To verify if the Aptoide page structure has changed and broken the parser, we have
        another set of integration tests.
        """
        page_contents: str
        with io.open("tests/resources/lords-mobile-contents.html", "r") as lords_file:
            page_contents = lords_file.read()
        svc = aptoide_service.AptoideService()

        details: AppDetails = svc._parse_soup(page_contents)
        assert details.name == "Lords Mobile"
        assert details.version == "2.104"
        assert details.downloads == "7.5M"
        assert details.release_date == "28-04-2023"
        self.assertTrue(
            details.description.startswith("Lords Mobile is a multiplayer online")
        )
        self.assertTrue(details.description.endswith("for you not to miss an enemy!"))
