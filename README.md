# 🔍 Verificador de Conteúdo Textual em Links com PDF e HTML

Este projeto permite analisar uma lista de links (em um arquivo Excel) e verificar se eles contêm um conjunto de palavras-chave fornecidas pelo usuário. Ele é capaz de ler tanto o conteúdo HTML da página quanto PDFs vinculados ou diretamente acessados.

---

## 🧠 Funcionalidades

- Detecta automaticamente se o link aponta para:
  - Um **PDF direto**
  - Um **PDF embutido na página HTML**
  - Ou apenas o **HTML da página**
- Extrai o texto do conteúdo e verifica a presença de **palavras-chave** definidas pelo usuário.
- Gera um novo arquivo `.xlsx` com os links que contêm **todos** os termos buscados.
- Exibe no terminal e no arquivo de saída:
  - Tempo de execução por link
  - Origem do conteúdo analisado
  - Palavras-chave encontradas

---

## 📁 Estrutura dos Arquivos

- `main.py` → Script principal. Responsável por coletar input do usuário e controlar o fluxo da aplicação.
- `verificador.py` → Módulo que contém a lógica para acessar os links e extrair o conteúdo.
- `requirements.txt` → Pacotes usados na aplicação.
- `Arquivo inserido com links` → Arquivo de entrada com uma coluna `link` contendo os URLs a serem analisados.
- `artigos_com_temas_correlatos.xlsx` → Arquivo de saída com os resultados.

---

## ▶️ Como usar

### 1. 📥 Pré-requisitos

Instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
