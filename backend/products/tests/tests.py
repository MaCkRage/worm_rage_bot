from unittest import TestCase

from rest_framework.test import APIClient

from products.tests.test_data import generate_update_products_data

client_api = APIClient()


class UpdateDataTest(TestCase):

    def setUp(self):
        self.data = generate_update_products_data(product_count=1000, sellers_count=5)

    def test_update_data(self):
        response = client_api.post(r'/api/products/update_products/', format='json',
                                   data=self.data)
        self.assertEqual(response.status_code, 201)
