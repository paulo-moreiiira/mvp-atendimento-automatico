
import pytest
from app import app


@pytest.fixture
def cliente():
    app.config["TESTING"] = True

    with app.test_client() as cliente:
        yield cliente


def test_pagina_inicial(cliente):
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"dispositivo" in resposta.data.lower()


@pytest.mark.parametrize(
    ("sistema", "aplicativo"),
    [
        ("Android", "XCIPTV"),
        ("iOS", "Smarters Player Lite"),
    ],
)
def test_recomendacao_celular(cliente, sistema, aplicativo):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Celular",
            "sistema": sistema,
            "marca": "",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert aplicativo in texto


def test_celular_sem_sistema(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Celular",
            "sistema": "",
            "marca": "",
        },
    )

    assert "Selecione o sistema do seu celular." in (
        resposta.get_data(as_text=True)
    )


@pytest.mark.parametrize(
    ("marca", "aplicativo"),
    [
        ("Samsung", "2TPlay"),
        ("LG", "Max+"),
        ("TCL", "XCIPTV"),
        ("Philco", "MAX+"),
        ("Philips", "XCIPTV"),
        ("Sony", "XCIPTV"),
        ("AOC", "XCIPTV"),
    ],
)
def test_recomendacao_smart_tv(cliente, marca, aplicativo):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": marca,
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert aplicativo in texto


def test_smart_tv_outra_marca(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": "Outra",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "Entre em contato com o vendedor" in texto


def test_smart_tv_sem_marca(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": "",
        },
    )

    assert "Selecione uma marca válida para sua Smart TV." in (
        resposta.get_data(as_text=True)
    )


def test_smart_tv_com_marca_invalida(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": "MarcaInventada",
        },
    )

    assert "Selecione uma marca válida para sua Smart TV." in (
        resposta.get_data(as_text=True)
    )


@pytest.mark.parametrize(
    ("sistema", "aplicativo"),
    [
        ("Android TV/Google TV", "XCIPTV"),
        ("Fire TV", "XCIPTV"),
        ("Roku", "Max+"),
    ],
)
def test_recomendacao_tv_box(cliente, sistema, aplicativo):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "TV Box",
            "sistema": sistema,
            "marca": "",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert aplicativo in texto


def test_tv_box_outro_sistema(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "TV Box",
            "sistema": "Outro",
            "marca": "",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "entre em contato com o vendedor" in texto


def test_tv_box_sem_sistema(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "TV Box",
            "sistema": "",
            "marca": "",
        },
    )

    assert "Selecione um sistema válido para sua TV Box." in (
        resposta.get_data(as_text=True)
    )


def test_tv_box_com_sistema_invalido(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "TV Box",
            "sistema": "SistemaInventado",
            "marca": "",
        },
    )

    assert "Selecione um sistema válido para sua TV Box." in (
        resposta.get_data(as_text=True)
    )


def test_dispositivo_invalido(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "",
            "sistema": "",
            "marca": "",
        },
    )

    assert "Selecione um dispositivo válido." in (
        resposta.get_data(as_text=True)
    )
