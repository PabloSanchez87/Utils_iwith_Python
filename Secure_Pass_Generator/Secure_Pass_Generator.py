import string
import random


length = int(input('Longitud de la constraseña: '))

characters = string.ascii_letters + string.digits + string.punctuation

password = "".join(random.choice(characters) for i in range(length))

print("La contraseña generada es: " + password)