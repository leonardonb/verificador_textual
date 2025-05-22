import pandas as pd
import os
from verificador import verificar_link
import tkinter as tk
from tkinter import filedialog

if __name__ == "__main__":
    print("Digite as palavras-chave separadas por vírgulas (ex: 'previdência social','brasileira'):")
    entrada = input("→ ").strip()
    keywords = [termo.strip().lower() for termo in entrada.split(",")]

    # Criar janela raiz do Tkinter
    root = tk.Tk()
    root.withdraw()  # Ocultar janela principal

    # Abrir diálogo para selecionar arquivo de entrada
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
        temas_correlatos.append(len(encontrados) == len(keywords))
        tempos.append(round(duracao, 2))

    df["origem_conteudo"] = resultados_origem
    df["termos_encontrados"] = resultados_encontrados
    df["temas_correlatos"] = temas_correlatos
    df["tempo_execucao_s"] = tempos

    print("Selecione onde deseja salvar o arquivo de saída:")
    nome_saida = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                              filetypes=[("Excel files", "*.xlsx")],
                                              title="Salvar como",
                                              initialfile="artigos_com_temas_correlatos.xlsx")

    if nome_saida:
        df[df["temas_correlatos"]].to_excel(nome_saida, index=False)
        print(f"\nResultados exportados para '{nome_saida}' com sucesso.")
    else:
        print("Nenhum arquivo de saída foi salvo.")
