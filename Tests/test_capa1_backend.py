import pytest
from src.backend import evaluar, ErrorExpresion


class TestSumasValidas:

    def test_suma_dos_enteros(self):
        assert evaluar("3 + 5") == 8.0

    def test_suma_tres_numeros(self):
        assert evaluar("1 + 2 + 3") == 6.0

    def test_suma_con_decimales(self):
        assert evaluar("1.5 + 2.5") == 4.0

    def test_numeros_grandes(self):
        assert evaluar("1000 + 2000 + 3000") == 6000.0

    def test_un_solo_numero(self):
        assert evaluar("42") == 42.0

    def test_cero_mas_cero(self):
        assert evaluar("0 + 0") == 0.0

    def test_espacios_extra(self):
        assert evaluar("  3  +  5  ") == 8.0


class TestValoresLimite:

    def test_limite_200_chars_valido(self):
        # 25 veces "1 + " da exactamente 100 chars, armamos expresión de ~200
        partes = ["1"] * 50
        expresion = " + ".join(partes)  # exactamente 200 chars
        expresion = expresion[:200]
        # Aseguramos que no termine en "+"
        expresion = expresion.strip().rstrip("+").strip()
        resultado = evaluar(expresion)
        assert resultado >= 1.0

    def test_limite_201_chars_invalido(self):
        expresion = "1" * 201
        with pytest.raises(ErrorExpresion):
            evaluar(expresion)


class TestExpresionesInvalidas:

    def test_expresion_vacia_lanza_error(self):
        with pytest.raises(ErrorExpresion):
            evaluar("")

    def test_solo_espacios_lanza_error(self):
        with pytest.raises(ErrorExpresion):
            evaluar("   ")

    def test_operadores_consecutivos(self):
        with pytest.raises(ErrorExpresion):
            evaluar("3 ++ 5")

    def test_empieza_con_mas(self):
        with pytest.raises(ErrorExpresion):
            evaluar("+ 3 + 5")

    def test_termina_con_mas(self):
        with pytest.raises(ErrorExpresion):
            evaluar("3 + 5 +")

    def test_multiplicacion_no_permitida(self):
        with pytest.raises(ErrorExpresion):
            evaluar("3 * 5")

    def test_resta_no_permitida(self):
        with pytest.raises(ErrorExpresion):
            evaluar("10 - 3")

    def test_letras_no_permitidas(self):
        with pytest.raises(ErrorExpresion):
            evaluar("tres + cinco")

    def test_inyeccion_de_codigo(self):
        with pytest.raises(ErrorExpresion):
            evaluar("__import__('os').system('ls')")

    def test_tipo_int_lanza_error(self):
        with pytest.raises(ErrorExpresion):
            evaluar(42)

    def test_tipo_none_lanza_error(self):
        with pytest.raises(ErrorExpresion):
            evaluar(None)


class TestParametricos:

    @pytest.mark.parametrize("expresion,esperado", [
        ("1 + 1", 2.0),
        ("10 + 10", 20.0),
        ("0 + 5", 5.0),
        ("2.5 + 2.5", 5.0),
        ("100 + 200 + 300", 600.0),
    ])
    def test_casos_validos(self, expresion, esperado):
        assert evaluar(expresion) == esperado

    @pytest.mark.parametrize("expresion", [
        "3 / 2",
        "abc",
        "",
        "3 ** 2",
        "3 - 1",
    ])
    def test_casos_invalidos(self, expresion):
        with pytest.raises(ErrorExpresion):
            evaluar(expresion)
