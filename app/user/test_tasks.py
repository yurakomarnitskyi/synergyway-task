from unittest.mock import patch, Mock
from django.test import TestCase
from user.tasks import fetch_and_save_next_user, fetch_and_save_address_for_user
from user.models import User, Address


class TasksTestCase(TestCase):
    @patch('user.tasks.requests.get')
    def test_fetch_and_save_next_user_mock(self, mock_get):
        user_response = Mock()
        user_response.json.return_value = [
            {'username': 'testuser', 'email': 'test@example.com', 'name': 'Test User'}
        ]
        user_response.status_code = 200

        address_response = Mock()
        address_response.json.return_value = [
            {
                'street': '123 Mock Street',
                'city': 'Mock City',
                'state': 'Mock State',
                'zip_code': '12345',
            }
        ]
        address_response.status_code = 200

        credit_card_response = Mock()
        credit_card_response.json.return_value = [
            {
                'credit_card_number': '1234567890123456',
                'expiration_date': '12/25/2025',
                'cardholder_name': 'Test User',
            }
        ]
        credit_card_response.status_code = 200

        mock_get.side_effect = [user_response, address_response, credit_card_response]

        fetch_and_save_next_user()

        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertEqual(mock_get.call_count, 3)

    @patch('user.tasks.requests.get')
    def test_fetch_address_mock(self, mock_get):
        user = User.objects.create(username='testuser', email='test@example.com')

        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'street': '123 Mock Street',
                'city': 'Mock City',
                'state': 'Mock State',
                'zip_code': '12345',
            }
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        fetch_and_save_address_for_user(user.id)

        address = Address.objects.get(user=user)
        self.assertEqual(address.street, '123 Mock Street')
        self.assertEqual(address.city, 'Mock City')
        mock_get.assert_called_once()
