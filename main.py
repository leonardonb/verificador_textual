# main.py
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog
from verificador import verificar_link
from busca import buscar_em_fontes
from app import iniciar_flask

def processar_links_excel(arquivo, termos):
    if not os.path.exists(arquivo):
        print(f"Arquivo '{arquivo}' não encontrado.")
        return

    df = pd.read_excel(arquivo)
    df = df.dropna(subset=["link"]).reset_index(drop=True)

    resultados_origem, resultados_encontrados, temas_correlatos, tempos = [], [], [], []

    for link in df["link"]:
        origem, encontrados, duracao = verificar_link(link, termos)
        resultados_origem.append(origem)
        resultados_encontrados.append(", ".join(encontrados))
        temas_correlatos.append("TEM" if len(encontrados) == len(termos) else "NÃO TEM")
        tempos.append(round(duracao, 2))

    df["origem_conteudo"] = resultados_origem
    df["temas_correlatos"] = temas_correlatos
    df["termos_encontrados"] = resultados_encontrados
    df["tempo_execucao_s"] = tempos

    nome_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if nome_saida:
        df.to_excel(nome_saida, index=False)
        print(f"Resultados salvos em '{nome_saida}'.")
    else:
        print("Salvamento cancelado.")

def main():
    print("Escolha o modo de execução:")
    print("1 - Interface terminal")
    print("2 - Interface Flask (web)")
    escolha_modo = input("→ ")

    if escolha_modo == "2":
        iniciar_flask()
        return

    print("\nDigite os termos separados por vírgulas (ex: 'previdência social, sustentabilidade'):")
    entrada = input("→ ")
    termos = [t.strip() for t in entrada.split(",") if t.strip()]
    if not termos:
        print("Nenhum termo válido informado.")
        return

    print("\nEscolha a fonte de links:")
    print("1 - Enviar um arquivo Excel")
    print("2 - Buscar artigos nos portais SciELO e Google Scholar")
    escolha = input("→ ")

    if escolha == "1":
        root = tk.Tk()
        root.withdraw()
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if caminho_arquivo:
            processar_links_excel(caminho_arquivo, termos)
        else:
            print("Nenhum arquivo selecionado.")

    elif escolha == "2":
        print("\nBuscando nas fontes...")
        df = buscar_em_fontes(termos)

        if df.empty:
            print("Nenhum resultado encontrado nas fontes.")
            return

        print("\nVerificando conteúdo dos links...")
        resultados_origem, resultados_encontrados, temas_correlatos, tempos = [], [], [], []

        for link in df["link"]:
            origem, encontrados, duracao = verificar_link(link, termos)
            resultados_origem.append(origem)
            resultados_encontrados.append(", ".join(encontrados))
            temas_correlatos.append("TEM" if len(encontrados) == len(termos) else "NÃO TEM")
            tempos.append(round(duracao, 2))

        df["origem_conteudo"] = resultados_origem
        df["temas_correlatos"] = temas_correlatos
        df["termos_encontrados"] = resultados_encontrados
        df["tempo_execucao_s"] = tempos

        print("\nEscolha onde deseja salvar o resultado:")
        root = tk.Tk()
        root.withdraw()
        caminho_saida = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if caminho_saida:
            df.to_excel(caminho_saida, index=False)
            print(f"Resultados salvos em '{caminho_saida}'.")
        else:
            print("Salvamento cancelado.")

    else:
        print("Opção inválida. Encerrando.")

if __name__ == "__main__":
    main()
