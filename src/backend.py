class ErrorExpresion(Exception):
    """Error que se lanza cuando la expresión es inválida."""
    pass


def evaluar(expresion: str) -> float:
    """
    Evalúa una expresión de suma y retorna el resultado como float.
    Solo soporta sumas con números positivos y decimales.
    NO usa eval() por seguridad.
    """
    # 1. Validar que sea string
    if not isinstance(expresion, str):
        raise ErrorExpresion("La expresión debe ser un string.")

    # 2. Validar longitud máxima
    if len(expresion) > 200:
        raise ErrorExpresion("La expresión es demasiado larga (máx 200 caracteres).")

    # 3. Validar que no esté vacía
    expresion_limpia = expresion.strip()
    if not expresion_limpia:
        raise ErrorExpresion("La expresión no puede estar vacía.")

    # 4. Validar que solo tenga dígitos, punto, + y espacios
    for char in expresion_limpia:
        if char not in "0123456789.+ ":
            raise ErrorExpresion(f"Carácter no permitido: '{char}'. Solo se permiten sumas.")

    # 5. Validar que no empiece ni termine con +
    if expresion_limpia.startswith("+"):
        raise ErrorExpresion("La expresión no puede empezar con '+'.")
    if expresion_limpia.endswith("+"):
        raise ErrorExpresion("La expresión no puede terminar con '+'.")

    # 6. Validar que no tenga operadores consecutivos (ej: ++ )
    if "++" in expresion_limpia:
        raise ErrorExpresion("La expresión no puede tener operadores consecutivos.")

    # 7. Calcular la suma dividiendo por '+'
    try:
        partes = expresion_limpia.split("+")
        resultado = sum(float(parte.strip()) for parte in partes)
        return resultado
    except ValueError:
        raise ErrorExpresion("La expresión contiene valores no numéricos.")
