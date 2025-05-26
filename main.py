import os
import pandas as pd
from verificador import verificar_link
from prisma import gerar_relatorio_prisma, gerar_fluxograma_prisma

def modo_terminal():
    import tkinter as tk
    from tkinter import filedialog

    print("Digite as palavras-chave separadas por vírgulas (ex: 'previdência social','série temporal'):")
    entrada = input("→ ").strip()
    keywords = [termo.strip() for termo in entrada.split(",")]

    root = tk.Tk()
    root.withdraw()
    print("Selecione o arquivo Excel com os links:")
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        print("Arquivo não selecionado ou não encontrado.")
        return

    df = pd.read_excel(caminho_arquivo)
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

    print("Selecione onde deseja salvar o arquivo Excel de saída:")
    nome_saida = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                              filetypes=[("Excel files", "*.xlsx")],
                                              title="Salvar como",
                                              initialfile="resultado_formatado.xlsx")
    if not nome_saida:
        print("Nenhum arquivo de saída foi salvo.")
        return

    with pd.ExcelWriter(nome_saida, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Resultado")
        workbook = writer.book
        worksheet = writer.sheets["Resultado"]
        formato_ok = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        formato_nok = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        col = df.columns.get_loc("temas_correlatos")
        worksheet.conditional_format(1, col, len(df), col, {'type': 'cell', 'criteria': '==', 'value': '"TEM"', 'format': formato_ok})
        worksheet.conditional_format(1, col, len(df), col, {'type': 'cell', 'criteria': '==', 'value': '"NÃO TEM"', 'format': formato_nok})

    resumo = gerar_relatorio_prisma(df)
    gerar_fluxograma_prisma(resumo)
    print(f"Resultados salvos com sucesso em {nome_saida}")

def iniciar_flask():
    import webbrowser
    from threading import Timer
    def abrir_navegador():
        webbrowser.open_new("http://localhost:5000")
    Timer(1, abrir_navegador).start()
    os.system("python app.py")

if __name__ == "__main__":
    print("Escolha o modo de execução:")
    print("[1] Modo terminal interativo")
    print("[2] Interface Web Flask")
    escolha = input("→ ").strip()

    if escolha == "1":
        modo_terminal()
    elif escolha == "2":
        iniciar_flask()
    else:
        print("Opção inválida.")
