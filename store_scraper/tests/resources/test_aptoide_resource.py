import json

from app import create_app
from app import create_app
from falcon import testing
from models.app_details import AppDetails
from services.aptoide_service import AptoideService
from unittest import TestCase
from unittest.mock import patch


class AptoideResourceTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = testing.TestClient(self.app)

    # Tests that a 400 error is returned when we call the /aptoide endpoint with a
    # search parameter not in the format of https://{app_name.en.aptoide.com/app}
    def test_on_get_invalid_url(self):
        response = self.client.simulate_get(
            "/aptoide?search=https://invalid-url.aptoide.com"
        )
        assert response.status_code == 400

    # Tests a valid url but mocks AppService.get_app_details to return a mock AppDetails
    # object. We are testing the Service internal methods in aptoide_service.py
    @patch.object(AptoideService, "get_app_details")
    def test_on_get_valid_url(self, get_app_details):
        mock_details = AppDetails(
            "Mock App", "1.23", "3.3M", "01-05-2023", "A Mock App"
        )
        get_app_details.return_value = mock_details

        expected_response = {
            "name": mock_details.name,
            "version": mock_details.version,
            "downloads": mock_details.downloads,
            "release_date": mock_details.release_date,
            "description": mock_details.description,
        }

        response = self.client.simulate_get(
            "/aptoide?search=https://mock-app.en.aptoide.com/app"
        )
        assert response.status_code == 200
        assert response.text == json.dumps(expected_response)
