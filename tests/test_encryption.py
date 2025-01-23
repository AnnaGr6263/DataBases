import unittest
import sys
import os

# Dodaj katalog główny projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.auth.encryption import hash_password
import bcrypt

class TestEncryption(unittest.TestCase):

    def test_hash_password(self):
        password = "securepassword123"
        hashed = hash_password(password)
        
        # Sprawdź, czy hasło jest poprawnie zahashowane
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))

    def test_hash_password_different(self):
        password1 = "securepassword123"
        password2 = "differentpassword456"
        hashed1 = hash_password(password1)
        hashed2 = hash_password(password2)
        
        # Sprawdź, czy różne hasła mają różne hashe
        self.assertNotEqual(hashed1, hashed2)
        self.assertTrue(bcrypt.checkpw(password1.encode('utf-8'), hashed1))
        self.assertTrue(bcrypt.checkpw(password2.encode('utf-8'), hashed2))

if __name__ == '__main__':
    unittest.main()
