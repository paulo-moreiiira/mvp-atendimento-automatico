from urllib.parse import quote

from flask import Flask, render_template, request

app = Flask(__name__)

WHATSAPP_NUMERO = "5531984539766"

MARCAS_VALIDAS = [
    "Samsung", "LG", "TCL", "Philco",
    "Philips", "Sony", "AOC", "Outra"
]

SISTEMAS_CELULAR = {
    "Android": "XCIPTV",
    "iOS": "Smarters Player Lite"
}

SISTEMAS_TV_BOX = {
    "Android TV/Google TV": "XCIPTV",
    "Fire TV": "XCIPTV",
    "Roku": "Max+",
    "Outro": None
}

APLICATIVOS_SMART_TV = {
    "Samsung": "2TPlay",
    "LG": "Max+",
    "TCL": "XCIPTV",
    "Philco": "MAX+",
    "Philips": "XCIPTV",
    "Sony": "XCIPTV",
    "AOC": "XCIPTV",
    "Outra": None
}

IMAGENS_APLICATIVOS = {
    "2TPlay": "2tplay.png",
    "Max+": "maxplus.png",
    "MAX+": "maxplus.png",
    "XCIPTV": "xciptv.png",
    "Smarters Player Lite": "smarters-player-lite.png",
}


def recomendar_aplicativo(dispositivo, sistema, marca):
    """Retorna o aplicativo indicado e a orientação correspondente."""
    if dispositivo == "Celular":
        if sistema not in SISTEMAS_CELULAR:
            return None, None, "Selecione o sistema do seu celular."
        aplicativo = SISTEMAS_CELULAR[sistema]
        orientacao = (
            f"Para seu celular ({sistema}), recomendamos o aplicativo "
            f"{aplicativo}. Procure pelo nome na loja oficial do aparelho."
        )
        return aplicativo, orientacao, None

    if dispositivo == "Smart TV":
        if marca not in MARCAS_VALIDAS:
            return None, None, "Selecione uma marca válida para sua Smart TV."
        aplicativo = APLICATIVOS_SMART_TV[marca]
        if not aplicativo:
            return None, (
                "Não temos uma recomendação automática para essa marca. "
                "Entre em contato com o vendedor para receber orientação."
            ), None
        orientacao = (
            f"Para sua Smart TV {marca}, recomendamos o aplicativo "
            f"{aplicativo}. Procure pelo nome na loja de aplicativos da "
            "televisão. A disponibilidade pode variar conforme o modelo."
        )
        return aplicativo, orientacao, None

    if dispositivo == "TV Box":
        if sistema not in SISTEMAS_TV_BOX:
            return None, None, "Selecione um sistema válido para sua TV Box."
        aplicativo = SISTEMAS_TV_BOX[sistema]
        if not aplicativo:
            return None, (
                "Para esse sistema, entre em contato com o vendedor para "
                "receber orientação sobre o aplicativo adequado."
            ), None
        orientacao = (
            f"Para sua TV Box com sistema {sistema}, recomendamos o "
            f"aplicativo {aplicativo}. Procure pelo nome na loja do aparelho."
        )
        return aplicativo, orientacao, None

    return None, None, "Selecione um dispositivo válido."


def criar_link_whatsapp(dados):
    linhas = [
        "Olá! Gostaria de continuar meu atendimento pela PHX Stream.",
        "",
        "INFORMAÇÕES DO APARELHO:",
        f"Dispositivo: {dados['dispositivo']}",
    ]
    if dados.get("marca"):
        linhas.append(f"Marca: {dados['marca']}")
    if dados.get("sistema"):
        linhas.append(f"Sistema: {dados['sistema']}")
    linhas.extend([
        f"Aplicativo recomendado: {dados.get('aplicativo') or 'Orientação necessária'}",
        f"Encontrou o aplicativo: {dados.get('encontrou') or 'Não informado'}",
        f"Conseguiu baixar/instalar: {dados.get('baixou') or 'Não se aplica'}",
        "",
        "Aguardo ajuda para continuar o atendimento.",
    ])
    return f"https://wa.me/{WHATSAPP_NUMERO}?text={quote(chr(10).join(linhas))}"


@app.route("/", methods=["GET", "POST"])
def inicio():
    dados = {
        "dispositivo": "",
        "sistema": "",
        "marca": "",
        "encontrou": "",
        "baixou": "",
    }
    etapa = "identificacao"
    aplicativo = None
    orientacao = None
    erro = None
    link_whatsapp = None
    imagem_aplicativo = None

    if request.method == "POST":
        for campo in dados:
            dados[campo] = request.form.get(campo, "").strip()
        etapa = request.form.get("etapa", "identificacao")
        aplicativo, orientacao, erro = recomendar_aplicativo(
            dados["dispositivo"], dados["sistema"], dados["marca"]
        )
        imagem_aplicativo = IMAGENS_APLICATIVOS.get(aplicativo)

        if not erro and etapa == "confirmacao":
            encontrou = dados["encontrou"]
            baixou = dados["baixou"]
            if encontrou not in {"Sim", "Não"}:
                erro = "Informe se conseguiu localizar o aplicativo."
            elif encontrou == "Sim" and baixou not in {"Sim", "Não"}:
                erro = "Informe se conseguiu baixar e instalar o aplicativo."
            elif encontrou == "Não":
                dados["baixou"] = "Não se aplica"
                link_whatsapp = criar_link_whatsapp(dados)
                etapa = "resumo"
            else:
                link_whatsapp = criar_link_whatsapp(dados)
                etapa = "resumo"
        elif not erro:
            etapa = "confirmacao"

    return render_template(
        "index.html",
        dados=dados,
        etapa=etapa,
        aplicativo=aplicativo,
        orientacao=orientacao,
        imagem_aplicativo=imagem_aplicativo,
        erro=erro,
        link_whatsapp=link_whatsapp,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)