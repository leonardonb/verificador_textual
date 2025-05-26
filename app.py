from flask import Flask, request, render_template, send_from_directory
import os
import pandas as pd
from verificador import verificar_link
from prisma import gerar_relatorio_prisma, gerar_fluxograma_prisma

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        arquivo = request.files["arquivo"]
        termos = request.form["termos"]

        if not arquivo or not termos:
            return "Por favor, envie um arquivo e os termos."

        caminho = os.path.join(app.config["UPLOAD_FOLDER"], arquivo.filename)
        arquivo.save(caminho)

        keywords = [t.strip() for t in termos.split(",")]
        df = pd.read_excel(caminho)

        df.attrs["identificados"] = len(df)
        df = df.dropna(subset=["link"]).reset_index(drop=True)

        resultados_origem, resultados_encontrados, temas_correlatos, tempos = [], [], [], []
        for link in df["link"]:
            origem, encontrados, duracao = verificar_link(link, keywords)
            resultados_origem.append(origem)
            resultados_encontrados.append(", ".join(encontrados))
            temas_correlatos.append("TEM" if len(encontrados) == len(keywords) else "NÃO TEM")
            tempos.append(round(duracao, 2))

        df["origem_conteudo"] = resultados_origem
        df["temas_correlatos"] = temas_correlatos
        df["termos_encontrados"] = resultados_encontrados
        df["tempo_execucao_s"] = tempos

        saida_excel = os.path.join(UPLOAD_FOLDER, "resultado_formatado.xlsx")
        with pd.ExcelWriter(saida_excel, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Resultado")
            workbook = writer.book
            worksheet = writer.sheets["Resultado"]
            formato_ok = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
            formato_nok = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
            col = df.columns.get_loc("temas_correlatos")
            worksheet.conditional_format(1, col, len(df), col, {'type': 'cell', 'criteria': '==', 'value': '"TEM"', 'format': formato_ok})
            worksheet.conditional_format(1, col, len(df), col, {'type': 'cell', 'criteria': '==', 'value': '"NÃO TEM"', 'format': formato_nok})

        resumo = gerar_relatorio_prisma(df, os.path.join(UPLOAD_FOLDER, "relatorio_prisma"))
        gerar_fluxograma_prisma(resumo, os.path.join(UPLOAD_FOLDER, "fluxograma_prisma"))

        return render_template("index.html", arquivos=[
            "resultado_formatado.xlsx",
            "relatorio_prisma.json",
            "relatorio_prisma.csv",
            "fluxograma_prisma.png"
        ])

    return render_template("index.html", arquivos=[])

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
