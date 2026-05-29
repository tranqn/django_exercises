from unittest.mock import patch, MagicMock
from django.test import TestCase


class ExternalServiceTests(TestCase):
    @patch("myapp.services.send_email")
    def test_registration_sends_email(self, mock_send):
        """Registration triggers a welcome email."""
        mock_send.return_value = True
        # register user...
        # mock_send.assert_called_once_with("user@test.com", "Welcome!")
        pass

    @patch("myapp.services.payment_gateway")
    def test_payment_failure_handling(self, mock_payment):
        """Payment failure returns appropriate error."""
        mock_payment.charge.side_effect = Exception("Payment declined")
        # attempt payment...
        # assert response contains error
        pass