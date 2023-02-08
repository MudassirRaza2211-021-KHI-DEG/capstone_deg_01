from unittest import TestCase

from fastapi.testclient import TestClient

from capstone_deg_01.carbon_moist_api.carbon_moist_data_extract_app import app

client = TestClient(app)


class TestExample(TestCase):
    def test_collect_moisturemate_data_response_200_and_logs(self):
        with self.assertLogs() as captured:
            response = client.post(
                "/api/fetch/moisturemate_data",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that we get OK (200) response.
        self.assertEqual(len(captured.records), 1)
        # Check that the correct message is logged
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received MoistureMate data: {'test_key': 'test_value'}",
        )

    def test_collect_carbonsense_data_response_200_and_logs(self):
        with self.assertLogs() as captured:
            response = client.post(
                "/api/fetch/carbonsense_data",
                json={"test_key": "test_value"},
            )
        assert response.status_code == 200
        # Check that we get OK (200) response.
        self.assertEqual(len(captured.records), 1)
        # Check that the correct message is logged
        self.assertEqual(
            captured.records[0].getMessage(),
            "Received CarbonSense data: {'test_key': 'test_value'}",
        )

    def test_invalid_endpoint_response_404(self):
        response = client.post(
            "/invalid_endpoint",
            json={"test_key": "test_value"},
        )
        # Check that we get Not Found (404) response.
        assert response.status_code == 404
