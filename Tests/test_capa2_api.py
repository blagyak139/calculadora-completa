import pytest


class TestSalud:

    def test_health_check(self, cliente_api):
        r = cliente_api.get("/salud")
        assert r.status_code == 200


class TestSumasValidas:

    def test_suma_simple_retorna_200(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "3 + 5"})
        assert r.status_code == 200
        assert r.json()["resultado"] == 8.0

    def test_resultado_es_float(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "10 + 20"})
        assert r.status_code == 200
        assert isinstance(r.json()["resultado"], float)

    def test_decimales(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "1.5 + 2.5"})
        assert r.status_code == 200
        assert pytest.approx(r.json()["resultado"]) == 4.0

    def test_un_solo_numero(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "42"})
        assert r.status_code == 200
        assert r.json()["resultado"] == 42.0

    def test_content_type_json(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "1 + 1"})
        assert r.status_code == 200
        assert "application/json" in r.headers["content-type"]


class TestExpresionesInvalidas:

    def test_expresion_vacia_retorna_400(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": ""})
        assert r.status_code == 400

    def test_operador_invalido_retorna_400(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "3 * 5"})
        assert r.status_code == 400

    def test_letras_retorna_400(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "tres + cinco"})
        assert r.status_code == 400

    def test_mensaje_descriptivo_en_400(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": "3 * 5"})
        assert r.status_code == 400
        assert "detail" in r.json()


class TestValidacionFastAPI:

    def test_sin_campo_dato_retorna_422(self, cliente_api):
        r = cliente_api.post("/sumar", json={})
        assert r.status_code == 422

    def test_campo_mal_nombrado_retorna_422(self, cliente_api):
        r = cliente_api.post("/sumar", json={"expression": "3 + 5"})
        assert r.status_code == 422

    def test_body_vacio_retorna_422(self, cliente_api):
        r = cliente_api.post("/sumar")
        assert r.status_code == 422

    def test_dato_numerico_no_retorna_500(self, cliente_api):
        r = cliente_api.post("/sumar", json={"dato": 12345})
        assert r.status_code != 500


class TestParametricos:

    @pytest.mark.parametrize("expresion,esperado", [
        ("1 + 1", 2.0),
        ("5 + 5", 10.0),
        ("0 + 0", 0.0),
        ("100 + 200", 300.0),
    ])
    def test_casos_validos(self, cliente_api, expresion, esperado):
        r = cliente_api.post("/sumar", json={"dato": expresion})
        assert r.status_code == 200
        assert r.json()["resultado"] == esperado

    @pytest.mark.parametrize("expresion", [
        "3 * 5",
        "abc",
        "",
        "3 - 1",
        "3 / 2",
    ])
    def test_casos_invalidos_nunca_500(self, cliente_api, expresion):
        r = cliente_api.post("/sumar", json={"dato": expresion})
        assert r.status_code == 400
        assert r.status_code != 500
