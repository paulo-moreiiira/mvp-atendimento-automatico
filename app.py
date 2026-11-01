
from flask import Flask, render_template, request

app = Flask(__name__)

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


@app.route("/", methods=["GET", "POST"])
def inicio():
    dispositivo = ""
    sistema = ""
    marca = ""
    orientacao = None
    aplicativo = None
    erro = None

    if request.method == "POST":
        dispositivo = request.form.get("dispositivo", "").strip()
        sistema = request.form.get("sistema", "").strip()
        marca = request.form.get("marca", "").strip()

        if dispositivo == "Celular":
            if sistema in SISTEMAS_CELULAR:
                aplicativo = SISTEMAS_CELULAR[sistema]
                orientacao = (
                    f"Para seu celular ({sistema}), recomendamos "
                    f"o aplicativo {aplicativo}. "
                    "Procure pelo nome do aplicativo na loja oficial "
                    "do seu aparelho."
                )
            else:
                erro = "Selecione o sistema do seu celular."

        elif dispositivo == "Smart TV":
            if marca in MARCAS_VALIDAS:
                aplicativo = APLICATIVOS_SMART_TV[marca]

                if aplicativo:
                    orientacao = (
                        f"Para sua Smart TV {marca}, recomendamos "
                        f"o aplicativo {aplicativo}. "
                        "Procure pelo nome na loja de aplicativos "
                        "da televisão. A disponibilidade pode variar "
                        "conforme o modelo."
                    )
                else:
                    orientacao = (
                        "Não temos uma recomendação automática "
                        "para essa marca. Entre em contato com "
                        "o vendedor para receber orientação."
                    )
            else:
                erro = "Selecione uma marca válida para sua Smart TV."

        elif dispositivo == "TV Box":
            if sistema in SISTEMAS_TV_BOX:
                aplicativo = SISTEMAS_TV_BOX[sistema]

                if aplicativo:
                    orientacao = (
                        f"Para sua TV Box com sistema {sistema}, "
                        f"recomendamos o aplicativo {aplicativo}. "
                        "Procure pelo nome na loja de aplicativos "
                        "do aparelho."
                    )
                else:
                    orientacao = (
                        "Para esse sistema, entre em contato com "
                        "o vendedor para receber orientação sobre "
                        "o aplicativo adequado."
                    )
            else:
                erro = "Selecione um sistema válido para sua TV Box."

        else:
            erro = "Selecione um dispositivo válido."

    return render_template(
        "index.html",
        dispositivo=dispositivo,
        sistema=sistema,
        marca=marca,
        orientacao=orientacao,
        aplicativo=aplicativo,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True)
