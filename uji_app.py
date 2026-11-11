
import unittest
from flask_app import app


class UjiAplikasi(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_dashboard(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_daftar_mahasiswa(self):
        response = self.client.get("/mahasiswa")
        self.assertEqual(response.status_code, 200)

    def test_filter_prodi(self):
        response = self.client.get("/mahasiswa?prodi=SI")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dewi Lestari", response.data)

    def test_detail_mahasiswa(self):
        response = self.client.get(
            "/mahasiswa/A11.2023.00001"
        )
        self.assertEqual(response.status_code, 200)

    def test_pencarian(self):
        response = self.client.post(
            "/cari",
            data={"nim": "A11.2023.00001"}
        )
        self.assertEqual(response.status_code, 302)

    def test_api_mahasiswa(self):
        response = self.client.get(
            "/api/mahasiswa/A11.2023.00001"
        )
        self.assertEqual(response.status_code, 200)

    def test_mahasiswa_tidak_ditemukan(self):
        response = self.client.get("/mahasiswa/12345")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
