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

@pytest.mark.parametrize(
    ("dispositivo", "sistema", "marca", "arquivo"),
    [
        ("Celular", "Android", "", "xciptv.png"),
        ("Celular", "iOS", "", "smarters-player-lite.png"),
        ("Smart TV", "", "Samsung", "2tplay.png"),
        ("Smart TV", "", "LG", "maxplus.png"),
        ("Smart TV", "", "TCL", "xciptv.png"),
        ("Smart TV", "", "Philco", "maxplus.png"),
        ("TV Box", "Android TV/Google TV", "", "xciptv.png"),
        ("TV Box", "Roku", "", "maxplus.png"),
    ],
)
def test_imagem_aplicativo_recomendado(
    cliente, dispositivo, sistema, marca, arquivo
):
    resposta = cliente.post(
        "/",
        data={
            "dispositivo": dispositivo,
            "sistema": sistema,
            "marca": marca,
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert f"/static/img/{arquivo}" in texto


def test_botao_whatsapp_na_recomendacao(cliente):
    resposta = cliente.post(
        "/",
        data={
            "etapa": "confirmacao",
            "dispositivo": "Celular",
            "sistema": "Android",
            "marca": "",
            "encontrou": "Não",
            "baixou": "",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert resposta.status_code == 200
    assert "Finalizar atendimento pelo WhatsApp" in texto
    assert "https://wa.me/5531984539766" in texto


def test_mensagem_preparada_no_whatsapp(cliente):
    resposta = cliente.post(
        "/",
        data={
            "etapa": "confirmacao",
            "dispositivo": "Celular",
            "sistema": "Android",
            "marca": "",
            "encontrou": "Não",
            "baixou": "",
        },
    )

    texto = resposta.get_data(as_text=True)

    assert "wa.me/5531984539766?text=" in texto
    assert "Encontrou%20o%20aplicativo" in texto
    assert "Dispositivo%3A%20Celular" in texto


def test_identidade_phx_stream_na_pagina_inicial(cliente):
    resposta = cliente.get("/")
    texto = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "PHX Stream" in texto
    assert "/static/img/logo-phx.png" in texto


def test_fluxo_mostra_pergunta_se_encontrou_aplicativo(cliente):
    resposta = cliente.post("/", data={
        "etapa": "identificacao",
        "dispositivo": "Smart TV",
        "marca": "Samsung",
        "sistema": "",
    })
    texto = resposta.get_data(as_text=True)
    assert "Você conseguiu localizar o aplicativo?" in texto
    assert "2TPlay" in texto


def test_fluxo_nao_encontrou_gera_resumo_e_link_whatsapp(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "Smart TV",
        "marca": "Samsung",
        "sistema": "",
        "encontrou": "Não",
        "baixou": "",
    })
    texto = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "RESUMO DO ATENDIMENTO" in texto
    assert "Encontrou o aplicativo?</dt><dd>Não</dd>" in texto
    assert "Não se aplica" in texto
    assert "https://wa.me/5531984539766" in texto
    assert "Finalizar atendimento pelo WhatsApp" in texto


def test_fluxo_encontrou_mas_nao_conseguiu_baixar(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "Celular",
        "sistema": "Android",
        "marca": "",
        "encontrou": "Sim",
        "baixou": "Não",
    })
    texto = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "Conseguiu baixar?" in texto
    assert "Não" in texto
    assert "wa.me/5531984539766" in texto


def test_fluxo_encontrou_e_baixou_aplicativo(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "TV Box",
        "sistema": "Roku",
        "marca": "",
        "encontrou": "Sim",
        "baixou": "Sim",
    })
    texto = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "Max+" in texto
    assert "Sim" in texto
    assert "wa.me/5531984539766" in texto


def test_fluxo_exige_resposta_sobre_localizacao(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "Celular",
        "sistema": "Android",
        "marca": "",
        "encontrou": "",
        "baixou": "",
    })
    assert "Informe se conseguiu localizar o aplicativo." in resposta.get_data(as_text=True)


def test_fluxo_exige_download_quando_encontrou(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "Celular",
        "sistema": "Android",
        "marca": "",
        "encontrou": "Sim",
        "baixou": "",
    })
    assert "Informe se conseguiu baixar e instalar o aplicativo." in resposta.get_data(as_text=True)


def test_aplicativo_indisponivel_pede_ajuda_sem_recomendacao(cliente):
    resposta = cliente.post("/", data={
        "etapa": "confirmacao",
        "dispositivo": "Smart TV",
        "marca": "Outra",
        "sistema": "",
        "encontrou": "Não",
        "baixou": "",
    })
    texto = resposta.get_data(as_text=True)
    assert resposta.status_code == 200
    assert "Orientação necessária" in texto
    assert "wa.me/5531984539766" in texto