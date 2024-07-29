import string
import secrets  # Utilizado para generar números aleatorios de manera segura,
                # adecuados para propósitos criptográficos.

def generate_password(length: int, use_letters=True, use_digits=True, use_punctuation=True) -> str:
    """
    Genera una contraseña segura con la longitud y tipos de caracteres especificados.
    
    Parámetros:
    - length (int): La longitud de la contraseña generada. Debe ser mayor que 0.
    - use_letters (bool): Incluir letras en la contraseña. Por defecto es True.
    - use_digits (bool): Incluir dígitos en la contraseña. Por defecto es True.
    - use_punctuation (bool): Incluir puntuación en la contraseña. Por defecto es True.
    
    Retorna:
    - str: La contraseña generada.
    
    Lanza:
    - ValueError: Si la longitud es menor o igual a 0, o si no se selecciona ningún tipo de carácter.
    """
    if length <= 0:
        raise ValueError("La longitud de la contraseña debe ser mayor que 0.")
    
    character_pool = ''
    if use_letters:
        character_pool += string.ascii_letters
    if use_digits:
        character_pool += string.digits
    if use_punctuation:
        character_pool += string.punctuation
    
    if not character_pool:
        raise ValueError("Se debe seleccionar al menos un tipo de carácter.")
    
    password = ''.join(secrets.choice(character_pool) for _ in range(length))
    return password



if __name__ == "__main__":
    try:
        length = int(input("Longitud de la contraseña: "))
        include_letters = input("¿Incluir letras? (yes/no): ").strip().lower() in ['yes', 'y']
        include_digits = input("¿Incluir dígitos? (yes/no): ").strip().lower() in ['yes', 'y']
        include_punctuation = input("¿Incluir puntuación? (yes/no): ").strip().lower() in ['yes', 'y']
        
        password = generate_password(length, include_letters, include_digits, include_punctuation)
        print("La contraseña generada es: " + password)
    except ValueError as e:
        print(f"Error: {e}")
