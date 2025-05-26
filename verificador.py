import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import time
from urllib.parse import urljoin
import unicodedata

def remover_acentos(txt):
    return ''.join(
        c for c in unicodedata.normalize('NFD', txt)
        if unicodedata.category(c) != 'Mn'
    )

def normalizar(texto):
    return remover_acentos(texto).lower()

def extrair_texto_pdf(url):
    try:
        resposta = requests.get(url, timeout=15)
        if resposta.status_code != 200:
            return ""
        with fitz.open(stream=resposta.content, filetype="pdf") as doc:
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
        return texto
    except Exception as e:
        print(f"Erro ao extrair PDF: {e}")
        return ""

def url_aponta_para_pdf(resposta, url):
    return (
            url.lower().endswith(".pdf") or
            resposta.headers.get("Content-Type", "").lower().startswith("application/pdf")
    )

def verificar_link(url, termos):
    inicio = time.time()
    try:
        resposta = requests.get(url, timeout=15, stream=True)
        if resposta.status_code != 200:
            print(f"[{url}] → ERRO {resposta.status_code} ({time.time() - inicio:.2f}s)")
            return "Erro", [], 0

        if url_aponta_para_pdf(resposta, url):
            print(f"[{url}] → A URL é um PDF direto.")
            texto = extrair_texto_pdf(url)
            origem = "PDF direto"
        else:
            soup = BeautifulSoup(resposta.content, "html.parser")
            pdf_url = None
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if ".pdf" in href.lower():
                    pdf_url = urljoin(url, href)
                    break
            if pdf_url:
                print(f"[{url}] → PDF encontrado dentro da página: {pdf_url}")
                texto = extrair_texto_pdf(pdf_url)
                origem = "PDF embutido"
            else:
                print(f"[{url}] → Nenhum PDF encontrado. Usando HTML.")
                texto = soup.get_text()
                origem = "HTML"

        texto_normalizado = normalizar(texto)
        encontrados = [termo for termo in termos if normalizar(termo) in texto_normalizado]
        resultado = "TEM" if len(encontrados) == len(termos) else "NÃO TEM"
        duracao = time.time() - inicio

        print(f"→ Origem: {origem}")
        print(f"→ {resultado} todos os temas correlatos")
        print(f"→ Encontrados: {', '.join(encontrados) if encontrados else 'nenhuma palavra-chave'}")
        print(f"→ Tempo: {duracao:.2f}s\n")

        return origem, encontrados, duracao
    except Exception as e:
        print(f"[{url}] → FALHA ({time.time() - inicio:.2f}s): {e}")
        return "Falha", [], 0
