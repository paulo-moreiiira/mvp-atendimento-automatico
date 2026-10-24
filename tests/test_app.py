
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


def test_celular_android(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Celular",
            "sistema": "Android",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    assert b"Android" in resposta.data


def test_celular_sem_sistema(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Celular",
            "sistema": "",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    assert b"Selecione o sistema do seu celular." in resposta.data



def test_dispositivo_invalido(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "",
            "sistema": "",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    texto = resposta.get_data(as_text=True)
    assert "Selecione um dispositivo válido." in texto

def test_celular_ios(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Celular",
            "sistema": "iOS",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    assert "iPhone (iOS)" in resposta.get_data(as_text=True)


def test_smart_tv_lg(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": "LG",
        },
    )

    assert resposta.status_code == 200
    assert "Smart TV da marca LG" in resposta.get_data(as_text=True)


def test_smart_tv_sem_marca(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "Smart TV",
            "sistema": "",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    assert "Selecione a marca da sua Smart TV." in resposta.get_data(as_text=True)


def test_tv_box_android(cliente):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": "TV Box",
            "sistema": "Android TV/Google TV",
            "marca": "",
        },
    )

    assert resposta.status_code == 200
    assert "TV Box com sistema Android TV/Google TV" in resposta.get_data(as_text=True)
