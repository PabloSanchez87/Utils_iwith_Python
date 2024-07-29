import unittest
import string
from secure_pass_generator import generate_password

class TestGeneratePassword(unittest.TestCase):

    def test_length(self):
        """Verifica que la longitud de la contraseña generada coincida con la longitud especificada.
        
        Se prueban longitudes de 1 a 100 para asegurarse de que la función genera contraseñas 
        de la longitud correcta.
        """
        for length in range(1, 101):  # Testing lengths from 1 to 100
            password = generate_password(length)
            self.assertEqual(len(password), length)

    def test_default_includes_all_characters(self):
        """Verifica que la contraseña por defecto incluya letras, dígitos y puntuación.
        
        Genera una contraseña con la longitud máxima probada (100) y verifica que 
        contenga al menos una letra, un dígito y un símbolo de puntuación.
        """
        password = generate_password(100)
        has_letter = any(c in string.ascii_letters for c in password)
        has_digit = any(c in string.digits for c in password)
        has_punctuation = any(c in string.punctuation for c in password)

        self.assertTrue(has_letter, "Password does not include letters.")
        self.assertTrue(has_digit, "Password does not include digits.")
        self.assertTrue(has_punctuation, "Password does not include punctuation.")

    def test_no_letters(self):
        """Verifica que la contraseña no incluya letras cuando `use_letters` es False.
        
        Genera una contraseña sin letras y verifica que no contenga ningún caracter alfabético.
        """
        password = generate_password(100, use_letters=False)
        has_letter = any(c in string.ascii_letters for c in password)
        self.assertFalse(has_letter, "Password includes letters when it should not.")

    def test_no_digits(self):
        """Verifica que la contraseña no incluya dígitos cuando `use_digits` es False.
        
        Genera una contraseña sin dígitos y verifica que no contenga ningún número.
        """
        password = generate_password(100, use_digits=False)
        has_digit = any(c in string.digits for c in password)
        self.assertFalse(has_digit, "Password includes digits when it should not.")

    def test_no_punctuation(self):
        """Verifica que la contraseña no incluya puntuación cuando `use_punctuation` es False.
        
        Genera una contraseña sin caracteres de puntuación y verifica que no contenga ninguno de estos símbolos.
        """
        password = generate_password(100, use_punctuation=False)
        has_punctuation = any(c in string.punctuation for c in password)
        self.assertFalse(has_punctuation, "Password includes punctuation when it should not.")

    def test_no_characters_selected(self):
        """Verifica que se lance una excepción si no se selecciona ningún tipo de carácter.
        
        Intenta generar una contraseña sin letras, dígitos ni puntuación, y verifica que se 
        lance un `ValueError`.
        """
        with self.assertRaises(ValueError):
            generate_password(10, use_letters=False, use_digits=False, use_punctuation=False)

    def test_invalid_length(self):
        """Verifica que se lance una excepción si se proporciona una longitud inválida.
        
        Prueba con longitudes de 0 y negativas, y verifica que se lance un `ValueError`.
        """
        with self.assertRaises(ValueError):
            generate_password(0)
        with self.assertRaises(ValueError):
            generate_password(-1)

if __name__ == '__main__':
    unittest.main()
