import pytest


# ── Helpers ─────────────────────────────────────────────────────────────────

def presionar(pagina, *botones):
    for testid in botones:
        pagina.click(f"[data-testid='{testid}']")

def leer_expresion(pagina):
    return pagina.input_value("#expresion")

def leer_resultado(pagina):
    return pagina.inner_text("#resultado")

def leer_error(pagina):
    return pagina.inner_text("#mensaje-error")


# ── Capa 3: Pruebas E2E ──────────────────────────────────────────────────────

class TestCargaInicial:

    def test_titulo_visible(self, pagina):
        assert "calculadora" in pagina.inner_text("h1").lower()

    def test_expresion_vacia_al_inicio(self, pagina):
        assert leer_expresion(pagina) == ""

    def test_resultado_vacio_al_inicio(self, pagina):
        assert leer_resultado(pagina) == ""

    def test_botones_numericos_visibles(self, pagina):
        for i in range(10):
            assert pagina.is_visible(f"[data-testid='btn-{i}']")

    def test_boton_mas_visible(self, pagina):
        assert pagina.is_visible("[data-testid='btn-mas']")

    def test_boton_igual_visible(self, pagina):
        assert pagina.is_visible("[data-testid='btn-igual']")


class TestInteraccionBotones:

    def test_clic_numero_actualiza_expresion(self, pagina):
        presionar(pagina, "btn-3")
        assert leer_expresion(pagina) == "3"

    def test_multiples_numeros_se_concatenan(self, pagina):
        presionar(pagina, "btn-1", "btn-2", "btn-3")
        assert leer_expresion(pagina) == "123"

    def test_boton_mas_agrega_operador(self, pagina):
        presionar(pagina, "btn-5", "btn-mas")
        assert "+" in leer_expresion(pagina)

    def test_mas_no_aparece_si_expresion_vacia(self, pagina):
        presionar(pagina, "btn-mas")
        assert leer_expresion(pagina) == ""

    def test_mas_no_se_duplica(self, pagina):
        presionar(pagina, "btn-3", "btn-mas", "btn-mas")
        expresion = leer_expresion(pagina)
        assert expresion.count("+") == 1

    def test_c_borra_todo(self, pagina):
        presionar(pagina, "btn-3", "btn-mas", "btn-5", "btn-borrar")
        assert leer_expresion(pagina) == ""
        assert leer_resultado(pagina) == ""


class TestFlujoCompleto:

    def test_flujo_3_mas_5_igual_8(self, pagina):
        presionar(pagina, "btn-3", "btn-mas", "btn-5", "btn-igual")
        pagina.wait_for_function(
            "document.getElementById('resultado').textContent !== ''"
        )
        assert float(leer_resultado(pagina)) == 8.0

    def test_flujo_10_mas_20_mas_30_igual_60(self, pagina):
        presionar(pagina, "btn-1", "btn-0",
                  "btn-mas",
                  "btn-2", "btn-0",
                  "btn-mas",
                  "btn-3", "btn-0",
                  "btn-igual")
        pagina.wait_for_function(
            "document.getElementById('resultado').textContent !== ''"
        )
        assert float(leer_resultado(pagina)) == 60.0

    def test_c_borra_resultado_previo(self, pagina):
        presionar(pagina, "btn-3", "btn-mas", "btn-5", "btn-igual")
        pagina.wait_for_function(
            "document.getElementById('resultado').textContent !== ''"
        )
        presionar(pagina, "btn-borrar")
        assert leer_resultado(pagina) == ""

    def test_segunda_operacion_reemplaza_resultado(self, pagina):
        presionar(pagina, "btn-1", "btn-mas", "btn-1", "btn-igual")
        pagina.wait_for_function(
            "document.getElementById('resultado').textContent !== ''"
        )
        presionar(pagina, "btn-borrar")
        presionar(pagina, "btn-3", "btn-mas", "btn-3", "btn-igual")
        pagina.wait_for_function(
            "document.getElementById('resultado').textContent !== ''"
        )
        assert float(leer_resultado(pagina)) == 6.0


class TestManejoErrores:

    def test_igual_sin_expresion_muestra_error(self, pagina):
        presionar(pagina, "btn-igual")
        assert leer_error(pagina) != ""

    def test_escribir_borra_el_error(self, pagina):
        presionar(pagina, "btn-igual")
        assert leer_error(pagina) != ""
        presionar(pagina, "btn-5")
        assert leer_error(pagina) == ""

    def test_resultado_vacio_si_expresion_vacia(self, pagina):
        presionar(pagina, "btn-igual")
        assert leer_resultado(pagina) == ""
