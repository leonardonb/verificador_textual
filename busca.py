import pandas as pd
import requests
from bs4 import BeautifulSoup
from scholarly import scholarly
import time

# =============================
# BUSCA EM PLATAFORMAS ACADÊMICAS
# =============================

def buscar_em_fontes(termos):
    """
    Realiza buscas reais no Google Scholar e SciELO usando os termos-chave.
    Retorna um DataFrame com colunas: título, ano, link.
    Usa lógica AND, e se nenhum resultado, tenta OR.
    Limita a até 100 resultados por fonte.
    """
    print("🔎 Iniciando busca real em plataformas acadêmicas...")
    resultados = []
    termos_and = " ".join(f"{t}" for t in termos)
    termos_or = " OR ".join(f"{t}" for t in termos)

    # === Google Scholar ===
    def buscar_google(query):
        encontrados = []
        try:
            busca = scholarly.search_pubs(query)
            for _ in range(100):
                try:
                    pub = next(busca)
                    if pub and 'bib' in pub:
                        titulo = pub['bib'].get('title', '')
                        ano = pub['bib'].get('pub_year', '')
                        link = pub.get('pub_url', '')
                        if link:
                            encontrados.append({"título": titulo, "ano": ano, "link": link})
                except StopIteration:
                    break
                except Exception:
                    continue
        except Exception as e:
            print(f"⚠️ Erro no Google Scholar: {e}")
        return encontrados

    # Primeiro com AND
    print(f"🔍 Google Scholar (AND) → {termos_and}")
    resultados_google = buscar_google(termos_and)
    if not resultados_google:
        print(f"🔄 Tentando Google Scholar com OR → {termos_or}")
        resultados_google = buscar_google(termos_or)

    resultados.extend(resultados_google)

    # === SciELO ===
    def buscar_scielo(query):
        encontrados = []
        try:
            url = f"https://search.scielo.org/?q={query.replace(' ', '+')}"
            resposta = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(resposta.content, "html.parser")
            artigos = soup.select("div.item")
            for artigo in artigos[:100]:
                titulo = artigo.select_one(".title")
                link_tag = titulo.find("a") if titulo else None
                ano_tag = artigo.select_one(".publication")
                link = link_tag["href"] if link_tag else ""
                titulo_txt = link_tag.text.strip() if link_tag else ""
                ano = ano_tag.text.strip()[-4:] if ano_tag else ""
                if link:
                    encontrados.append({"título": titulo_txt, "ano": ano, "link": link})
        except Exception as e:
            print(f"⚠️ Erro ao buscar no SciELO: {e}")
        return encontrados

    print(f"📘 SciELO (AND) → {termos_and}")
    resultados_scielo = buscar_scielo(termos_and)
    if not resultados_scielo:
        print(f"🔄 Tentando SciELO com OR → {termos_or}")
        resultados_scielo = buscar_scielo(termos_or)

    resultados.extend(resultados_scielo)

    if not resultados:
        print("⚠️ Nenhum link encontrado.")
        return pd.DataFrame()

    df = pd.DataFrame(resultados).drop_duplicates(subset=["link"])
    return df


def salvar_em_excel(df1, df2=None, caminho="resultados_busca_academica.xlsx"):
    if df2 is not None:
        df_comb = pd.concat([df1, df2]).drop_duplicates(subset=["link"])
    else:
        df_comb = df1
    df_comb.to_excel(caminho, index=False)
    print(f"💾 Resultados salvos em {caminho}")
