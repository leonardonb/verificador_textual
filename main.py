import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from verificador import verificar_link

if __name__ == "__main__":
    print("Digite as palavras-chave separadas por vírgulas (ex: 'previdência social','brasileira'):")
    entrada = input("→ ").strip()
    keywords = [termo.strip().strip("'\"").lower() for termo in entrada.split(",")]

    root = tk.Tk()
    root.withdraw()
    print("Selecione o arquivo Excel com os links:")
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        print("Arquivo não selecionado ou não encontrado.")
        exit()

    df = pd.read_excel(caminho_arquivo)

    resultados_origem = []
    resultados_encontrados = []
    temas_correlatos = []
    tempos = []

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

    print("Selecione onde deseja salvar o arquivo de saída:")
    nome_saida = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                              filetypes=[("Excel files", "*.xlsx")],
                                              title="Salvar como",
                                              initialfile="analise_links_completa.xlsx")

    if not nome_saida:
        print("Nenhum arquivo de saída foi salvo.")
        exit()

    # Escrever com formatação usando xlsxwriter
    with pd.ExcelWriter(nome_saida, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Resultado")
        workbook = writer.book
        worksheet = writer.sheets["Resultado"]

        # Estilo para "TEM" (verde) e "NÃO TEM" (vermelho)
        format_tema_ok = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        format_tema_nok = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})

        col_idx = df.columns.get_loc("temas_correlatos")

        # Formatação exata para "TEM"
        worksheet.conditional_format(1, col_idx, len(df), col_idx, {
            'type': 'cell',
            'criteria': '==',
            'value': '"TEM"',
            'format': format_tema_ok
        })

        # Formatação exata para "NÃO TEM"
        worksheet.conditional_format(1, col_idx, len(df), col_idx, {
            'type': 'cell',
            'criteria': '==',
            'value': '"NÃO TEM"',
            'format': format_tema_nok
        })

    print(f"Resultados exportados com formatação para '{nome_saida}'")