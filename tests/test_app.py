import unittest
from app import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"DevOps Dashboard", response.data)

    def test_health_json(self):
        response = self.app.get("/health.json", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"healthy", response.data)

    def test_stats_json(self):
        response = self.app.get("/stats.json", headers={"Accept": "application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"total_requests", response.data)

    def test_404_page(self):
        response = self.app.get("/nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)

if __name__ == "__main__":
    unittest.main()
