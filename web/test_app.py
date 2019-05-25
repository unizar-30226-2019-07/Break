import unittest
from flask import url_for
from urllib.parse import urlparse
from app import app


class AnonymousUser(unittest.TestCase):

	def setUp(self):
		self.client = app.test_client()
		self.app_context = app.test_request_context()
		self.app_context.push()
		self.client.testing = True

	def login(self, email, password):
		return self.client.post('/login', data=dict(email=email, password=password))

	def logout(self):
		return self.client.get('/logout')

	def test_login_logout(self):

		response = self.login(app.config['USERNAME'], app.config['PASSWORD'])
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, url_for('index'))

		response = self.logout()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, url_for('index'))

		response = self.login(app.config['USERNAME'] + 'x', app.config['PASSWORD'])
		self.assertIn('Credenciales incorrectas', str(response.data))

		response = self.login(app.config['USERNAME'], app.config['PASSWORD'] + 'x')
		self.assertIn('Credenciales incorrectas', str(response.data))

	def test_home_page(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 200)

	def test_products_page(self):
		response = self.client.get('/listings')
		self.assertEqual(response.status_code, 200)

	def test_product_page(self):
		response = self.client.get('/single/787')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Mercedes-Benz', str(response.data))

	def test_auctions_page(self):
		response = self.client.get('/auctions')
		self.assertEqual(response.status_code, 200)

	def test_auction_page(self):
		response = self.client.get('/auction/935')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Aston Martin', str(response.data))

	def test_user_page(self):
		response = self.client.get('/user/573')
		self.assertEqual(response.status_code, 302)
		self.assertEqual(urlparse(response.location).path, url_for('login'))

class Ordinary(unittest.TestCase):

	@classmethod
	def login(cls, email, password):
		return cls.client.post('/login', data=dict(email=email, password=password))

	@classmethod
	def logout(cls):
		return cls.client.get('/logout')

	@classmethod
	def setUpClass(cls):
		cls.client = app.test_client()
		cls.app_context = app.test_request_context()
		cls.app_context.push()
		cls.client.testing = True
		cls.login(app.config['USERNAME'], app.config['PASSWORD'])

	@classmethod
	def tearDownClass(cls):
		cls.logout()

	def test_user_page(self):
		response = self.client.get('/user/573')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Testing Purposes', str(response.data))

	def test_user_page(self):
		response = self.client.get('/user/573')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Testing Purposes', str(response.data))

	def test_product_page(self):
		response = self.client.get('/single/574')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Gato de Cheshire', str(response.data))
		self.assertIn('Editar producto', str(response.data))

	def test_auction_page(self):
		response = self.client.get('/auction/576')
		self.assertEqual(response.status_code, 200)
		self.assertIn('Restaurante italiano', str(response.data))
		self.assertIn('Editar subasta', str(response.data))

if __name__ == "__main__":
    unittest.main()
