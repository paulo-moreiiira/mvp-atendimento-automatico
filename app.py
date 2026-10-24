
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():
    dispositivo = ""
    sistema = ""
    marca = ""
    orientacao = None
    erro = None

    if request.method == "POST":
        dispositivo = request.form.get("dispositivo", "")
        sistema = request.form.get("sistema", "")
        marca = request.form.get("marca", "")

        if dispositivo == "Celular":
            if sistema == "Android":
                orientacao = (
                    "Você utiliza Android. O próximo passo é verificar "
                    "qual aplicativo é compatível com seu aparelho."
                )
            elif sistema == "iOS":
                orientacao = (
                    "Você utiliza iPhone (iOS). O próximo passo é verificar "
                    "qual aplicativo é compatível com seu aparelho."
                )
            else:
                erro = "Selecione o sistema do seu celular."

        elif dispositivo == "Smart TV":
            marcas_validas = [
                "Samsung", "LG", "TCL", "Philco", "Philips",
                "Sony", "AOC", "Hisense", "Panasonic", "Outra"
            ]

            if marca in marcas_validas:
                orientacao = (
                    f"Você selecionou uma Smart TV da marca {marca}. "
                    "Agora é necessário verificar a compatibilidade "
                    "do aplicativo com o modelo da televisão."
                )
            else:
                erro = "Selecione a marca da sua Smart TV."

        elif dispositivo == "TV Box":
            sistemas_validos = [
                "Android TV/Google TV", "Fire TV", "Roku", "Outro"
            ]

            if sistema in sistemas_validos:
                orientacao = (
                    f"Você selecionou uma TV Box com sistema {sistema}. "
                    "O próximo passo é verificar a compatibilidade "
                    "do aparelho e orientar a instalação."
                )
            else:
                erro = "Selecione o sistema da sua TV Box."

        else:
            erro = "Selecione um dispositivo válido."

    return render_template(
        "index.html",
        dispositivo=dispositivo,
        sistema=sistema,
        marca=marca,
        orientacao=orientacao,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True)
