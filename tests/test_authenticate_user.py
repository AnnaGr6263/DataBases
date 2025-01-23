import unittest
import sys
import os
from unittest.mock import patch

# Dodaj katalog główny projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth.authenticate_user import authenticate_user

class TestAuthenticateUser(unittest.TestCase):

    @patch('src.db.fetch.fetch_users')
    def test_authenticate_user_success(self, mock_fetch_users):
        mock_fetch_users.return_value = [
            {'username': 'testuser', 'hashed_password': '$2b$12$KIX/8J1G1Q9Q1Q9Q1Q9Q1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u'}
        ]
        password = 'securepassword123'
        hashed_password = '$2b$12$KIX/8J1G1Q9Q1Q9Q1Q9Q1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u'
        self.assertTrue(authenticate_user('testuser', password))

    @patch('src.db.fetch.fetch_users')
    def test_authenticate_user_failure(self, mock_fetch_users):
        mock_fetch_users.return_value = [
            {'username': 'testuser', 'hashed_password': '$2b$12$KIX/8J1G1Q9Q1Q9Q1Q9Q1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u1u'}
        ]
        password = 'wrongpassword'
        self.assertFalse(authenticate_user('testuser', password))

    @patch('src.db.fetch.fetch_users')
    def test_authenticate_user_nonexistent(self, mock_fetch_users):
        mock_fetch_users.return_value = []
        password = 'securepassword123'
        self.assertFalse(authenticate_user('nonexistentuser', password))

if __name__ == '__main__':
    unittest.main()
